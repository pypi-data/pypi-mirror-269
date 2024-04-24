from ldap3 import Connection
from ldap3 import Server
from ldap3 import ALL, NTLM
from ldap3.core.exceptions import LDAPBindError, LDAPConfigurationParameterError, LDAPException
from pprint import pprint as prettyprint


# creating a settings object primarily to remove django dependency for this file.  The intent is to separate the
#   django stuff to another file so this file can be easily debugged and tested.  This will mean, however, there
#   will be an additional step to move django settings to LdapConfig settings in django_backend.
class LdapConfig:
    # config will allow these settings to be passed on init
    # NOTE: choosing to use named params instead of dict, so it is discoverable in IDE
    def __init__(self,
                 host: str = None, port: int = None, use_ssl: bool = True, use_ntlm: bool = True,
                 user_field_dn: str = None, user_field_groups_dn: str = None,
                 user_attributes: [str] or None = None,
                 bind_user: str = None, bind_password: str = None,
                 user_search_dn: str = None, user_search_query: str = None,
                 ntlm_domain: str = None, ntlm_prefix: str = None):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.use_ntlm = use_ntlm
        self.user_field_dn = user_field_dn or 'distinguishedName'
        self.user_field_groups_dn = user_field_groups_dn or 'memberOf'
        self.bind_user = bind_user
        self.bind_password = bind_password
        self.user_search_dn = user_search_dn
        self.user_search_query = user_search_query
        self.ntlm_domain = ntlm_domain
        self.ntlm_prefix = ntlm_prefix
        # self.user_attributes = ["*"]
        self.user_attributes = user_attributes or [
            'distinguishedName',
            'cn',
            'givenName',
            'sn',
            'mail',
            'c',
            'st',
            'l',
            'department',
            'title',
            'sAMAccountName',
            'manager',
            'memberOf',
        ]


class LdapUser:
    """
    LdapUser is an abstraction of a ldap user search result after authentication; the intent is to provide the basic
        means to work with a user more pythonic than a ldap3 search result.  I think it is going to be a thin wrapper
        with a couple of helper properties and methods.
        Goals:
            - make it easier to work with pythonic properties by throwing away ldap metadata except the value
            - make constructor properties for knowing the dn field and the groups field with reasonable defaults
            - add guaranteed property for is_authenticated
            - add guaranteed private property _groups defaulted to empty list
            - add helper method to convert ldap group dn's to list of group names (more pythonic)
                Ex: ["CN=MY_GROUP,OU=DALLAS,OU=OFFICES,OU=EXAMPLE,OU=ORG"] -> ["MY_GROUP"]
            - add helper method for returning if a group exists in the _groups list (True/False)
            - add helper method for returning if dn contains an organizational unit (OU=<stuff>) (True/False)
    """
    def __init__(self, user_field_dn: str = 'distinguishedName', user_field_groups_dn: str = 'memberOf'):
        # we need to know the dn field and groups field for this implementation (defaults to inetorg and inetorgperson)
        self._field_dn = user_field_dn
        self._field_groups_dn = user_field_groups_dn
        # authenticated is marked after binding successfully with provided password
        self.is_authenticated = False

    def get_groups(self) -> [str]:
        """
        parses a list of group_dn's and extracts them to a list of group names for the self._groups property
        :param group_dn_list: list of group_dn's
        :return: None
        """
        _groups = []
        groups_dn = getattr(self, self._field_groups_dn, [])
        for group_dn in groups_dn:
            # ex dn: CN=ProjectOnlineResources,OU=GROUPS,OU=ASIA,OU=OFFICES,DC=example,DC=org
            # grab everything before the first comma
            cn_part = str(group_dn)[:str(group_dn).index(',')].strip().upper()
            if cn_part.startswith('CN='):
                cn_part = cn_part[3:]
            _groups.append(cn_part)
        return _groups

    def get_dn(self):
        return getattr(self, self._field_dn, None)

    def has_group(self, group_name: str) -> bool:
        if group_name in self.get_groups():
            return True
        return False

    def has_ou(self, ou_name: str) -> bool:
        ou_check = ou_name or ''
        dn = self.get_dn() or ''
        dn_parts = dn.split(',')
        for dn_part in dn_parts:
            if dn_part.startswith('OU='):
                if str(dn_part[3:]).strip().lower() == ou_check.lower():
                    return True
        return False

    @staticmethod
    def get_ldap_attr(ldap_data_dict, attr_name:str, default_value=None):
        attr = getattr(ldap_data_dict, attr_name, default_value)
        if attr != default_value:
            return getattr(attr, 'value', default_value)

    def load(self, ldap_data_dict):
        # instead of hard coding lets loop over the user attributes passed in
        if ldap_data_dict and ldap_data_dict.entry_attributes:
            # if we pass a * this doesn't work
            #   need to read atts dynamically so * works

            atts = ldap_data_dict.entry_attributes
            for att in atts:
                setattr(self, att, self.get_ldap_attr(ldap_data_dict, att, None))

        # if ldap_data_dict:
        #     self.dn = self.get_ldap_attr(ldap_data_dict, 'distinguishedName', None)  # ldap_data_dict.distinguishedName.value
        #     self.cn = self.get_ldap_attr(ldap_data_dict, 'cn', None)  # ldap_data_dict.cn.value
        #     self.gn = self.get_ldap_attr(ldap_data_dict, 'givenName', None)  # ldap_data_dict.givenName.value
        #     self.sn = self.get_ldap_attr(ldap_data_dict, 'sn', None)  # ldap_data_dict.sn.value
        #     self.email = self.get_ldap_attr(ldap_data_dict, 'mail', None)  # ldap_data_dict.mail.value
        #     self.country_code = self.get_ldap_attr(ldap_data_dict, 'c', None)  # ldap_data_dict.c.value
        #     self.state_code = self.get_ldap_attr(ldap_data_dict, 'st', None)  # ldap_data_dict.st.value
        #     self.city = self.get_ldap_attr(ldap_data_dict, 'l', None)  # ldap_data_dict.l.value
        #     self.department = self.get_ldap_attr(ldap_data_dict, 'department', None)  # ldap_data_dict.department.value
        #     self.title = self.get_ldap_attr(ldap_data_dict, 'title', None)  # ldap_data_dict.title.value
        #     self.login = self.get_ldap_attr(ldap_data_dict, 'sAMAccountName', None)  # ldap_data_dict.sAMAccountName.value
        #     self.manager_dn = self.get_ldap_attr(ldap_data_dict, 'manager', None)  # ldap_data_dict.manager.value
        #     self.groups_dn = self.get_ldap_attr(ldap_data_dict, 'memberOf', [])  # ldap_data_dict.memberOf.value

    def pprint(self):
        prettyprint(vars(self))

    def __str__(self):
        return str(vars(self))


# trying generic LDAP authentication
class LdapAuthenticator:
    """
    LdapAuthenticator will utilise basic LDAP connection for binding and searching; must know DN for bind user and
        or user logging in.  This can work for deployed machines using a bind user, however, ActiveDirectory is
        better generally since it is based on the login which we always know when a user tries to log in.
    """

    def __init__(self, config: LdapConfig = None):
        self.config = config or LdapConfig()

    def validate_config(self):
        # validate our settings to use for connecting
        missing_error = 'setting was not found or passed as parameter during initialization'
        if not self.config.host:
            raise LDAPConfigurationParameterError(f'LDAP_HOST {missing_error}')
        if not self.config.user_search_dn:
            raise LDAPConfigurationParameterError(f'LDAP_USER_SEARCH_DN {missing_error}')
        if not self.config.user_search_query:
            raise LDAPConfigurationParameterError(f'LDAP_USER_SEARCH_QUERY {missing_error}')
        # Unlike connecting with NTLM we need the full DN for a user which we can't create from the login; as
        #   such we MUST bind using a bind_user_dn and bind_user_password.  We will then need to re-bind as
        #   the user once we get the users dn from searching.
        if not self.config.use_ntlm and not self.config.bind_user:
            raise LDAPConfigurationParameterError(f'LDAP_BIND_DN {missing_error}')
        if not self.config.use_ntlm and not self.config.bind_password:
            raise LDAPConfigurationParameterError(f'LDAP_BIND_PASSWORD {missing_error}')

    def find_user(self, login: str) -> LdapUser:
        # validate config
        self.validate_config()
        # validate credentials
        if not login:
            raise LDAPConfigurationParameterError('you must provide a login to authenticate')
        # get a connection to the ldap server
        server = Server(self.config.host, port=self.config.port, use_ssl=self.config.use_ssl, get_info=ALL)
        # we will either search the Directory for this user/password using LDAP or overridden NTLM protocol
        return self.search(server, login, "")

    def authenticate(self, login: str, password: str) -> LdapUser:
        # validate config
        self.validate_config()
        # validate credentials
        if not login:
            raise LDAPConfigurationParameterError('you must provide a login to authenticate')
        if not password:
            raise LDAPConfigurationParameterError('you must provide a password to authenticate')
        # get a connection to the ldap server
        server = Server(self.config.host, port=self.config.port, use_ssl=self.config.use_ssl, get_info=ALL)
        # we will either search the Directory for this user/password using LDAP or overridden NTLM protocol
        return self.search(server, login, password)

    def search(self, server: Server, login: str, password: str) -> LdapUser:
        ldap_user = LdapUser(user_field_dn=self.config.user_field_dn,
                             user_field_groups_dn=self.config.user_field_groups_dn)
        # Unlike AD; we always have to bind with a bind user to find the dn for the user with that login
        with Connection(server, self.config.bind_user, self.config.bind_password) as bind_conn:
            # we are bound as our bind user lets query the attributes of the login user
            bind_conn.search(self.config.user_search_dn, self.config.user_search_query.format(login),
                             attributes=self.config.user_attributes)
            # print(bind_conn)
            # print(bind_conn.entries)
            if bind_conn.entries:
                user_dn = bind_conn.entries[0]
            if user_dn:
                ldap_user.load(user_dn)
            if password and ldap_user.get_dn():
                # one additional step that is not needed for AD; re-bind as user now that we have dn to set is_authenticated
                #   since we originally bound as a bind user we haven't verified the password yet
                with Connection(server, ldap_user.get_dn(), password) as conn:
                    if conn.bound:
                        ldap_user.is_authenticated = True
        return ldap_user


# moving the operations for AD to a class
class ActiveDirectoryAuthenticator(LdapAuthenticator):
    """
    ActiveDirectoryAuthenticator will use NTLM (users login) to connect and search instead of normal LDAP DN
    """

    def fix_login(self, login):
        """
        Fix the passed login to work as needed
        NOTE: currently only need to reformat if using NTLM
        :param login: passed login
        :return: formatted login
        """
        if self.config.use_ntlm and login:
            if self.config.ntlm_domain and '\\' not in login:
                login = f'{self.config.ntlm_domain}\\{login}'
            if self.config.ntlm_prefix and not login.startswith(self.config.ntlm_prefix):
                login = f'{self.config.ntlm_prefix}{login}'
        return login

    def search(self, server: Server, login: str, password: str) -> LdapUser:
        ldap_user = LdapUser(user_field_dn=self.config.user_field_dn,
                             user_field_groups_dn=self.config.user_field_groups_dn)
        # try to bind with the user/pass given; test bad user bad password
        with Connection(server, user=self.fix_login(login), password=password, authentication=NTLM, auto_bind="NONE") as conn:
            conn.bind()
            if conn.bound:
                ldap_user.is_authenticated = True
                # print(f'connection bound: {conn.bound}')
                # print(f'whoami: {conn.extend.standard.who_am_i()}')
                # query this persons attributes to fill our LdapUser object
                conn.search(self.config.user_search_dn, self.config.user_search_query.format(login),
                            attributes=self.config.user_attributes)
                # todo: instead of all attributes above build out the specific list here if it is faster
                # attributes=['cn', 'distinguishedName', 'email'])
                # print(conn)
                # print(conn.entries)
                if conn.entries:
                    user_dn = conn.entries[0]

                if user_dn:
                    ldap_user.load(user_dn)
                    # print(f'user_dn: {user_dn}')
                    # ldap_user.pprint()
            else:
                raise LDAPBindError('Provided username and password are incorrect!')
        return ldap_user
