# NOTE: separating the django stuff from base ldap/ntlm stuff so testing is easier
import uuid
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User, Group
from django.conf import settings
from .ldap3 import LdapConfig, ActiveDirectoryAuthenticator, LdapAuthenticator, LDAPException


# CUSTOM BACKEND ADMIN OVERRIDE
class LdapBackend(BaseBackend):
    """
    Custom Backend to use the proper authenticator to try and login through external LDAP server and make sure the
        django user/groups objects are synced when logging into the admin
    """
    @staticmethod
    def load_config() -> LdapConfig:
        """
        Loads the LdapConfig using django settings
        NOTE: some properties are dependent on AD vs LDAP; so type test has to come first
        :return: populated ldap config object
        """
        auth_type = getattr(settings, 'LDAP_AUTHENTICATION', 'AD')
        return LdapConfig(
            host=getattr(settings, 'LDAP_HOST', None),
            port=getattr(settings, 'LDAP_PORT', None),
            use_ssl=getattr(settings, 'LDAP_USE_SSL', True),
            bind_user=getattr(settings, 'LDAP_BIND_DN', None),
            bind_password=getattr(settings, 'LDAP_BIND_PASSWORD', None),
            user_field_dn=getattr(settings, 'LDAP_USER_FIELD_DN', None),
            user_field_groups_dn=getattr(settings, 'LDAP_USER_FIELD_GROUPS_DN', None),
            user_search_dn=getattr(settings, 'LDAP_USER_SEARCH_DN', None),
            user_search_query=getattr(settings, 'LDAP_USER_SEARCH_QUERY', None),
            use_ntlm=(auth_type.lower().strip() == 'ad'),
            ntlm_domain=getattr(settings, 'AD_DOMAIN', None),
            ntlm_prefix=getattr(settings, 'AD_USER_ID_PREFIX', None),
        )

    @staticmethod
    def is_staff(ldap_user) -> bool:
        """
        uses ldap_user to define logic for if this django user should have the staff checked

        :param ldap_user: LdapUser instance
        :return: True/False
        """
        if ldap_user and ldap_user.has_ou('STAFF'):
            return True
        return False

    @staticmethod
    def is_it(ldap_user) -> bool:
        """
        uses ldap_user to define logic for if this django user is in the IT department

        :param ldap_user: LdapUser instance
        :return: True/False
        """
        if ldap_user:
            dpmt = getattr(ldap_user, 'department', '')
            if dpmt.strip().lower() == 'it':
                return True
        return False

    @staticmethod
    def is_super_user(ldap_user) -> bool:
        """
        uses ldap_user to define logic for if this django user should have the super_user checked

        :param ldap_user: LdapUser instance
        :return: True/False
        """
        if ldap_user and ldap_user.has_group('DJANGO_SUPER_USERS'):
            return True
        return False

    @staticmethod
    def get_password(ldap_user) -> str:
        return str(uuid.uuid4())

    @staticmethod
    def get_email(ldap_user) -> str:
        return getattr(ldap_user, 'mail', None) or ''

    @staticmethod
    def get_first(ldap_user) -> str:
        return getattr(ldap_user, 'givenName', None) or ''

    @staticmethod
    def get_last(ldap_user) -> str:
        return getattr(ldap_user, 'sn', None) or ''

    def authenticate(self, request, **kwargs):
        """
        Required for django to perform new authentications to our backend.
        NOTE: still required to have a get_user below to complete the authentication flow successfully
        :param request: the request
        :param kwargs: named parameters passed through from the request
        :return: new updated django user
        """
        # username and password should be passed by login in kwargs
        # print(kwargs)
        # print(f"username: {kwargs.get('username')}")
        # print(f"password: {kwargs.get('password')}")
        username = kwargs.get('username')
        password = kwargs.get('password')
        # check the username/password and return the user
        config = self.load_config()
        if config.use_ntlm:
            authenticator = ActiveDirectoryAuthenticator(config)
        else:
            authenticator = LdapAuthenticator(config)

        try:
            ldap_user = authenticator.authenticate(username, password)
            # ldap_user.pprint()
        except LDAPException as lex:
            # we don't want to error on username/password problems as this will fall through to local password
            if 'username and password are incorrect' not in str(lex):
                print('Exception loading user record from LDAP')
                print(lex)
            return None
        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            if ldap_user.is_authenticated:
                # Create a new user. Let's set a hash password since it will fall back to django if AD is down.
                user = User(username=username)
                # we assume if they can authenticate with AD they are able to get to admin (staff is checked)
                #   since even contractors work on our behalf even if they aren't technically staff
                user.is_staff = self.is_staff(ldap_user)
                user.is_superuser = self.is_super_user(ldap_user)
                user.username = username
                user.set_password(self.get_password(ldap_user))
                user.email = self.get_email(ldap_user)
                user.first_name = self.get_first(ldap_user)
                user.last_name = self.get_last(ldap_user)
                user.save()
        finally:
            # if we have a user and an ldap_user lets setup the groups
            if user and ldap_user.is_authenticated:
                # convert to strip() upper() so we have case insensitive matching
                authenticated_groups = getattr(settings, 'LDAP_AUTHENTICATED_GROUPS', [])
                try:
                    iter(authenticated_groups)
                except TypeError:
                    print(f'LDAP_AUTHENTICATED_GROUPS setting was not iterable; resetting to empty array!')
                    authenticated_groups = []

                # get a list of groups that match our ldap groups ignoring case
                app_groups = Group.objects.all()
                ldap_groups = ldap_user.get_groups()
                for group in app_groups:
                    # NOTE: ldap groups are case-insensitive; authenticated groups are exact match
                    igroup = group.name.strip().upper()
                    if igroup in ldap_groups or group.name in authenticated_groups:
                        # add these groups to the user if they don't exist
                        if group not in user.groups.all():
                            print(f'adding {group.name} to user...')
                            user.groups.add(group)
                            user.save()
                        else:
                            print(f'user already in {group.name}; skipping...')
        return user

    def get_user(self, user_id):
        """
        Required method for django to call to return a user based on id; if we don't have this we accept new
            authentications, but we won't be able to return the existing django user afterward, so it will stay on the
            login.
        :param user_id: this could be the id
        :return: user object or None
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
