Date: 2016-08-10
Title: salt valid opts
Tags: Salt
sulg: salt_valid_opts



/u01/github/salt-develop/salt/config/__init__.py 
```python

VALID_OPTS = {
    # The address of the salt master. May be specified as IP address or hostname
    'master': (string_types, list),

    # The TCP/UDP port of the master to connect to in order to listen to publications
    'master_port': int,

    # The behaviour of the minion when connecting to a master. Can specify 'failover',
    # 'disable' or 'func'. If 'func' is specified, the 'master' option should be set to an
    # exec module function to run to determine the master hostname. If 'disable' is specified
    # the minion will run, but will not try to connect to a master.
    'master_type': str,

    # Specify the format in which the master address will be specified. Can
    # specify 'default' or 'ip_only'. If 'ip_only' is specified, then the
    # master address will not be split into IP and PORT.
    'master_uri_format': str,

    # The fingerprint of the master key may be specified to increase security. Generate
    # a master fingerprint with `salt-key -F master`
    'master_finger': str,

    # Selects a random master when starting a minion up in multi-master mode
    'master_shuffle': bool,

    # When in multi-master mode, temporarily remove a master from the list if a conenction
    # is interrupted and try another master in the list.
    'master_alive_interval': int,

    # When in multi-master failover mode, fail back to the first master in the list if it's back
    # online.
    'master_failback': bool,

    # When in multi-master mode, and master_failback is enabled ping the top master with this
    # interval.
    'master_failback_interval': int,

    # The name of the signing key-pair
    'master_sign_key_name': str,

    # Sign the master auth-replies with a cryptographic signature of the masters public key.
    'master_sign_pubkey': bool,

    # Enables verification of the master-public-signature returned by the master in auth-replies.
    # Must also set master_sign_pubkey for this to work
    'verify_master_pubkey_sign': bool,

    # If verify_master_pubkey_sign is enabled, the signature is only verified, if the public-key of the master changes.
    # If the signature should always be verified, this can be set to True.
    'always_verify_signature': bool,

    # The name of the file in the masters pki-directory that holds the pre-calculated signature of the masters public-key.
    'master_pubkey_signature': str,

    # Instead of computing the signature for each auth-reply, use a pre-calculated signature.
    # The master_pubkey_signature must also be set for this.
    'master_use_pubkey_signature': bool,

    # The key fingerprint of the higher-level master for the syndic to verify it is talking to the intended
    # master
    'syndic_finger': str,

    # The user under which the daemon should run
    'user': str,

    # The root directory prepended to these options: pki_dir, cachedir,
    # sock_dir, log_file, autosign_file, autoreject_file, extension_modules,
    # key_logfile, pidfile:
    'root_dir': str,

    # The directory used to store public key data
    'pki_dir': str,

    # A unique identifier for this daemon
    'id': str,

    # The directory to store all cache files.
    'cachedir': str,

    # Flag to cache jobs locally.
    'cache_jobs': bool,

    # The path to the salt configuration file
    'conf_file': str,

    # The directory containing unix sockets for things like the event bus
    'sock_dir': str,

    # Specifies how the file server should backup files, if enabled. The backups
    # live in the cache dir.
    'backup_mode': str,

    # A default renderer for all operations on this host
    'renderer': str,

    # Renderer whitelist. The only renderers from this list are allowed.
    'renderer_whitelist': list,

    # Rendrerer blacklist. Renderers from this list are disalloed even if specified in whitelist.
    'renderer_blacklist': list,

    # A flag indicating that a highstate run should immediately cease if a failure occurs.
    'failhard': bool,

    # A flag to indicate that highstate runs should force refresh the modules prior to execution
    'autoload_dynamic_modules': bool,

    # Force the minion into a single environment when it fetches files from the master
    'environment': str,

    # Force the minion into a single pillar root when it fetches pillar data from the master
    'pillarenv': str,

    # Allows a user to provide an alternate name for top.sls
    'state_top': str,

    'state_top_saltenv': str,

    # States to run when a minion starts up
    'startup_states': str,

    # List of startup states
    'sls_list': list,

    # A top file to execute if startup_states == 'top'
    'top_file': str,

    # Location of the files a minion should look for. Set to 'local' to never ask the master.
    'file_client': str,

    # When using a local file_client, this parameter is used to allow the client to connect to
    # a master for remote execution.
    'use_master_when_local': bool,

    # A map of saltenvs and fileserver backend locations
    'file_roots': dict,

    # A map of saltenvs and fileserver backend locations
    'pillar_roots': dict,

    # The type of hashing algorithm to use when doing file comparisons
    'hash_type': str,

    # FIXME Does not appear to be implemented
    'disable_modules': list,

    # FIXME Does not appear to be implemented
    'disable_returners': list,

    # Tell the loader to only load modules in this list
    'whitelist_modules': list,

    # A list of additional directories to search for salt modules in
    'module_dirs': list,

    # A list of additional directories to search for salt returners in
    'returner_dirs': list,

    # A list of additional directories to search for salt states in
    'states_dirs': list,

    # A list of additional directories to search for salt grains in
    'grains_dirs': list,

    # A list of additional directories to search for salt renderers in
    'render_dirs': list,

    # A list of additional directories to search for salt outputters in
    'outputter_dirs': list,

    # A list of additional directories to search for salt utilities in. (Used by the loader
    # to populate __utils__)
    'utils_dirs': list,

    # salt cloud providers
    'providers': dict,

    # First remove all modules during any sync operation
    'clean_dynamic_modules': bool,

    # A flag indicating that a master should accept any minion connection without any authentication
    'open_mode': bool,

    # Whether or not processes should be forked when needed. The alternative is to use threading.
    'multiprocessing': bool,

    # Whether or not the salt minion should run scheduled mine updates
    'mine_enabled': bool,

    # Whether or not scheduled mine updates should be accompanied by a job return for the job cache
    'mine_return_job': bool,

    # Schedule a mine update every n number of seconds
    'mine_interval': int,

    # The ipc strategy. (i.e., sockets versus tcp, etc)
    'ipc_mode': str,

    # Enable ipv6 support for daemons
    'ipv6': bool,

    # The chunk size to use when streaming files with the file server
    'file_buffer_size': int,

    # The TCP port on which minion events should be published if ipc_mode is TCP
    'tcp_pub_port': int,

    # The TCP port on which minion events should be pulled if ipc_mode is TCP
    'tcp_pull_port': int,

    # The TCP port on which events for the master should be pulled if ipc_mode is TCP
    'tcp_master_pub_port': int,

    # The TCP port on which events for the master should be pulled if ipc_mode is TCP
    'tcp_master_pull_port': int,

    # The TCP port on which events for the master should pulled and then republished onto
    # the event bus on the master
    'tcp_master_publish_pull': int,

    # The TCP port for mworkers to connect to on the master
    'tcp_master_workers': int,

    # The file to send logging data to
    'log_file': str,

    # The level of verbosity at which to log
    'log_level': str,

    # The log level to log to a given file
    'log_level_logfile': str,

    # The format to construct dates in log files
    'log_datefmt': str,

    # The dateformat for a given logfile
    'log_datefmt_logfile': str,

    # The format for console logs
    'log_fmt_console': str,

    # The format for a given log file
    'log_fmt_logfile': (tuple, str),

    # A dictionary of logging levels
    'log_granular_levels': dict,

    # If an event is above this size, it will be trimmed before putting it on the event bus
    'max_event_size': int,

    # Always execute states with test=True if this flag is set
    'test': bool,

    # Tell the loader to attempt to import *.pyx cython files if cython is available
    'cython_enable': bool,

    # Tell the loader to attempt to import *.zip archives
    'enable_zip_modules': bool,

    # Tell the client to show minions that have timed out
    'show_timeout': bool,

    # Tell the client to display the jid when a job is published
    'show_jid': bool,

    # Tells the highstate outputter to show successful states. False will omit successes.
    'state_verbose': bool,

    # Specify the format for state outputs. See highstate outputter for additional details.
    'state_output': str,

    # Tells the highstate outputter to only report diffs of states that changed
    'state_output_diff': bool,

    # When true, states run in the order defined in an SLS file, unless requisites re-order them
    'state_auto_order': bool,

    # Fire events as state chunks are processed by the state compiler
    'state_events': bool,

    # The number of seconds a minion should wait before retry when attempting authentication
    'acceptance_wait_time': float,

    # The number of seconds a minion should wait before giving up during authentication
    'acceptance_wait_time_max': float,

    # Retry a connection attempt if the master rejects a minion's public key
    'rejected_retry': bool,

    # The interval in which a daemon's main loop should attempt to perform all necessary tasks
    # for normal operation
    'loop_interval': float,

    # Perform pre-flight verification steps before daemon startup, such as checking configuration
    # files and certain directories.
    'verify_env': bool,

    # The grains dictionary for a minion, containing specific "facts" about the minion
    'grains': dict,

    # Allow a daemon to function even if the key directories are not secured
    'permissive_pki_access': bool,

    # The path to a directory to pull in configuration file includes
    'default_include': str,

    # If a minion is running an esky build of salt, upgrades can be performed using the url
    # defined here. See saltutil.update() for additional information
    'update_url': (bool, string_types),

    # If using update_url with saltutil.update(), provide a list of services to be restarted
    # post-install
    'update_restart_services': list,

    # The number of seconds to sleep between retrying an attempt to resolve the hostname of a
    # salt master
    'retry_dns': float,

    # set the zeromq_reconnect_ivl option on the minion.
    # http://lists.zeromq.org/pipermail/zeromq-dev/2011-January/008845.html
    'recon_max': float,

    # If recon_randomize is set, this specifies the lower bound for the randomized period
    'recon_default': float,

    # Tells the minion to choose a bounded, random interval to have zeromq attempt to reconnect
    # in the event of a disconnect event
    'recon_randomize': bool,

    'return_retry_timer': int,
    'return_retry_timer_max': int,

    # Specify a returner in which all events will be sent to. Requires that the returner in question
    # have an event_return(event) function!
    'event_return': str,

    # The number of events to queue up in memory before pushing them down the pipe to an event returner
    # specified by 'event_return'
    'event_return_queue': int,

    # Only forward events to an event returner if it matches one of the tags in this list
    'event_return_whitelist': list,

    # Events matching a tag in this list should never be sent to an event returner.
    'event_return_blacklist': list,

    # default match type for filtering events tags: startswith, endswith, find, regex, fnmatch
    'event_match_type': str,

    # This pidfile to write out to when a daemon starts
    'pidfile': str,

    # Used with the SECO range master tops system
    'range_server': str,

    # The tcp keepalive interval to set on TCP ports. This setting can be used to tune salt connectivity
    # issues in messy network environments with misbehaving firewalls
    'tcp_keepalive': bool,

    # Sets zeromq TCP keepalive idle. May be used to tune issues with minion disconnects
    'tcp_keepalive_idle': float,

    # Sets zeromq TCP keepalive count. May be used to tune issues with minion disconnects
    'tcp_keepalive_cnt': float,

    # Sets zeromq TCP keepalive interval. May be used to tune issues with minion disconnects.
    'tcp_keepalive_intvl': float,

    # The network interface for a daemon to bind to
    'interface': str,

    # The port for a salt master to broadcast publications on. This will also be the port minions
    # connect to to listen for publications.
    'publish_port': int,

    # TODO unknown option!
    'auth_mode': int,

    # Set the zeromq high water mark on the publisher interface.
    # http://api.zeromq.org/3-2:zmq-setsockopt
    'pub_hwm': int,

    # ZMQ HWM for SaltEvent pub socket
    'salt_event_pub_hwm': int,
    # ZMQ HWM for EventPublisher pub socket
    'event_publisher_pub_hwm': int,

    # The number of MWorker processes for a master to startup. This number needs to scale up as
    # the number of connected minions increases.
    'worker_threads': int,

    # The port for the master to listen to returns on. The minion needs to connect to this port
    # to send returns.
    'ret_port': int,

    # The number of hours to keep jobs around in the job cache on the master
    'keep_jobs': int,

    # A master-only copy of the file_roots dictionary, used by the state compiler
    'master_roots': dict,

    # Add the proxymodule LazyLoader object to opts.  This breaks many things
    # but this was the default pre 2015.8.2.  This should default to
    # False in 2016.3.0
    'add_proxymodule_to_opts': bool,
    'git_pillar_base': str,
    'git_pillar_branch': str,
    'git_pillar_env': str,
    'git_pillar_root': str,
    'git_pillar_ssl_verify': bool,
    'git_pillar_global_lock': bool,
    'git_pillar_user': str,
    'git_pillar_password': str,
    'git_pillar_insecure_auth': bool,
    'git_pillar_privkey': str,
    'git_pillar_pubkey': str,
    'git_pillar_passphrase': str,
    'gitfs_remotes': list,
    'gitfs_mountpoint': str,
    'gitfs_root': str,
    'gitfs_base': str,
    'gitfs_user': str,
    'gitfs_password': str,
    'gitfs_insecure_auth': bool,
    'gitfs_privkey': str,
    'gitfs_pubkey': str,
    'gitfs_passphrase': str,
    'gitfs_env_whitelist': list,
    'gitfs_env_blacklist': list,
    'gitfs_ssl_verify': bool,
    'gitfs_global_lock': bool,
    'gitfs_saltenv': list,
    'hgfs_remotes': list,
    'hgfs_mountpoint': str,
    'hgfs_root': str,
    'hgfs_base': str,
    'hgfs_branch_method': str,
    'hgfs_env_whitelist': list,
    'hgfs_env_blacklist': list,
    'svnfs_remotes': list,
    'svnfs_mountpoint': str,
    'svnfs_root': str,
    'svnfs_trunk': str,
    'svnfs_branches': str,
    'svnfs_tags': str,
    'svnfs_env_whitelist': list,
    'svnfs_env_blacklist': list,
    'minionfs_env': str,
    'minionfs_mountpoint': str,
    'minionfs_whitelist': list,
    'minionfs_blacklist': list,

    # Specify a list of external pillar systems to use
    'ext_pillar': list,

    # Reserved for future use to version the pillar structure
    'pillar_version': int,

    # Whether or not a copy of the master opts dict should be rendered into minion pillars
    'pillar_opts': bool,

    # Cache the master pillar to disk to avoid having to pass through the rendering system
    'pillar_cache': bool,

    # Pillar cache TTL, in seconds. Has no effect unless `pillar_cache` is True
    'pillar_cache_ttl': int,

    # Pillar cache backend. Defaults to `disk` which stores caches in the master cache
    'pillar_cache_backend': str,

    'pillar_safe_render_error': bool,

    # When creating a pillar, there are several strategies to choose from when
    # encountering duplicate values
    'pillar_source_merging_strategy': str,

    # Recursively merge lists by aggregating them instead of replacing them.
    'pillar_merge_lists': bool,

    # How to merge multiple top files from multiple salt environments
    # (saltenvs); can be 'merge' or 'same'
    'top_file_merging_strategy': str,

    # The ordering for salt environment merging, when top_file_merging_strategy
    # is set to 'same'
    'env_order': list,

    # The salt environment which provides the default top file when
    # top_file_merging_strategy is set to 'same'; defaults to 'base'
    'default_top': str,

    'ping_on_rotate': bool,
    'peer': dict,
    'preserve_minion_cache': bool,
    'syndic_master': (string_types, list),

    # The behaviour of the multimaster syndic when connection to a master of masters failed. Can
    # specify 'random' (default) or 'ordered'. If set to 'random' masters will be iterated in random
    # order if 'ordered' the configured order will be used.
    'syndic_failover': str,
    'runner_dirs': list,
    'client_acl': dict,
    'client_acl_blacklist': dict,
    'publisher_acl': dict,
    'publisher_acl_blacklist': dict,
    'sudo_acl': bool,
    'external_auth': dict,
    'token_expire': int,
    'token_expire_user_override': (bool, dict),
    'file_recv': bool,
    'file_recv_max_size': int,
    'file_ignore_regex': (list, string_types),
    'file_ignore_glob': (list, string_types),
    'fileserver_backend': list,
    'fileserver_followsymlinks': bool,
    'fileserver_ignoresymlinks': bool,
    'fileserver_limit_traversal': bool,

    # The number of open files a daemon is allowed to have open. Frequently needs to be increased
    # higher than the system default in order to account for the way zeromq consumes file handles.
    'max_open_files': int,

    # Automatically accept any key provided to the master. Implies that the key will be preserved
    # so that subsequent connections will be authenticated even if this option has later been
    # turned off.
    'auto_accept': bool,
    'autosign_timeout': int,

    # A mapping of external systems that can be used to generate topfile data.
    'master_tops': dict,

    # A flag that should be set on a top-level master when it is ordering around subordinate masters
    # via the use of a salt syndic
    'order_masters': bool,

    # Whether or not to cache jobs so that they can be examined later on
    'job_cache': bool,

    # Define a returner to be used as an external job caching storage backend
    'ext_job_cache': str,

    # Specify a returner for the master to use as a backend storage system to cache jobs returns
    # that it receives
    'master_job_cache': str,

    # Specify whether the master should store end times for jobs as returns come in
    'job_cache_store_endtime': bool,

    # The minion data cache is a cache of information about the minions stored on the master.
    # This information is primarily the pillar and grains data. The data is cached in the master
    # cachedir under the name of the minion and used to predetermine what minions are expected to
    # reply from executions.
    'minion_data_cache': bool,

    # The number of seconds between AES key rotations on the master
    'publish_session': int,

    # Defines a salt reactor. See http://docs.saltstack.com/en/latest/topics/reactor/
    'reactor': list,

    # The TTL for the cache of the reactor configuration
    'reactor_refresh_interval': int,

    # The number of workers for the runner/wheel in the reactor
    'reactor_worker_threads': int,

    # The queue size for workers in the reactor
    'reactor_worker_hwm': int,

    # Defines engines. See https://docs.saltstack.com/en/latest/topics/engines/
    'engines': list,

    'serial': str,
    'search': str,

    # The update interval, in seconds, for the master maintenance process to update the search
    # index
    'search_index_interval': int,

    # A compound target definition. See: http://docs.saltstack.com/en/latest/topics/targeting/nodegroups.html
    'nodegroups': dict,

    # List-only nodegroups for salt-ssh. Each group must be formed as either a
    # comma-separated list, or a YAML list.
    'ssh_list_nodegroups': dict,

    # By default, salt-ssh uses its own specially-generated RSA key to auth
    # against minions. If this is set to True, salt-ssh will look in
    # for a key at ~/.ssh/id_rsa, and fall back to using its own specially-
    # generated RSA key if that file doesn't exist.
    'ssh_use_home_key': bool,

    # The logfile location for salt-key
    'key_logfile': str,

    # The source location for the winrepo sls files
    # (used by win_pkg.py, minion only)
    'winrepo_source_dir': str,

    'winrepo_dir': str,
    'winrepo_dir_ng': str,
    'winrepo_cachefile': str,
    'winrepo_remotes': list,
    'winrepo_remotes_ng': list,
    'winrepo_branch': str,
    'winrepo_ssl_verify': bool,
    'winrepo_user': str,
    'winrepo_password': str,
    'winrepo_insecure_auth': bool,
    'winrepo_privkey': str,
    'winrepo_pubkey': str,
    'winrepo_passphrase': str,

    # Set a hard limit for the amount of memory modules can consume on a minion.
    'modules_max_memory': int,

    # The number of minutes between the minion refreshing its cache of grains
    'grains_refresh_every': int,

    # Use lspci to gather system data for grains on a minion
    'enable_lspci': bool,

    # The number of seconds for the salt client to wait for additional syndics to
    # check in with their lists of expected minions before giving up
    'syndic_wait': int,

    # If this is set to True leading spaces and tabs are stripped from the start
    # of a line to a block.
    'jinja_lstrip_blocks': bool,

    # If this is set to True the first newline after a Jinja block is removed
    'jinja_trim_blocks': bool,

    # Cache minion ID to file
    'minion_id_caching': bool,

    # If set, the master will sign all publications before they are sent out
    'sign_pub_messages': bool,

    # The size of key that should be generated when creating new keys
    'keysize': int,

    # The transport system for this daemon. (i.e. zeromq, raet, etc)
    'transport': str,

    # The number of seconds to wait when the client is requesting information about running jobs
    'gather_job_timeout': int,

    # The number of seconds to wait before timing out an authentication request
    'auth_timeout': int,

    # The number of attempts to authenticate to a master before giving up
    'auth_tries': int,

    # The number of attempts to connect to a master before giving up.
    # Set this to -1 for unlimited attempts. This allows for a master to have
    # downtime and the minion to reconnect to it later when it comes back up.
    # In 'failover' mode, it is the number of attempts for each set of masters.
    # In this mode, it will cycle through the list of masters for each attempt.
    'master_tries': int,

    # Never give up when trying to authenticate to a master
    'auth_safemode': bool,

    'random_master': bool,

    # An upper bound for the amount of time for a minion to sleep before attempting to
    # reauth after a restart.
    'random_reauth_delay': int,

    # The number of seconds for a syndic to poll for new messages that need to be forwarded
    'syndic_event_forward_timeout': float,

    # The length that the syndic event queue must hit before events are popped off and forwarded
    'syndic_jid_forward_cache_hwm': int,

    'ssh_passwd': str,
    'ssh_port': str,
    'ssh_sudo': bool,
    'ssh_timeout': float,
    'ssh_user': str,
    'ssh_scan_ports': str,
    'ssh_scan_timeout': float,
    'ssh_identities_only': bool,

    # Enable ioflo verbose logging. Warning! Very verbose!
    'ioflo_verbose': int,

    'ioflo_period': float,

    # Set ioflo to realtime. Useful only for testing/debugging to simulate many ioflo periods very quickly.
    'ioflo_realtime': bool,

    # Location for ioflo logs
    'ioflo_console_logdir': str,

    # The port to bind to when bringing up a RAET daemon
    'raet_port': int,
    'raet_alt_port': int,
    'raet_mutable': bool,
    'raet_main': bool,
    'raet_clear_remotes': bool,
    'raet_clear_remote_masters': bool,
    'raet_road_bufcnt': int,
    'raet_lane_bufcnt': int,
    'cluster_mode': bool,
    'cluster_masters': list,
    'sqlite_queue_dir': str,

    'queue_dirs': list,

    # Instructs the minion to ping its master(s) ever n number of seconds. Used
    # primarily as a mitigation technique against minion disconnects.
    'ping_interval': int,

    # Instructs the salt CLI to print a summary of a minion responses before returning
    'cli_summary': bool,

    # The maximum number of minion connections allowed by the master. Can have performance
    # implications in large setups.
    'max_minions': int,


    'username': str,
    'password': str,

    # Use zmq.SUSCRIBE to limit listening sockets to only process messages bound for them
    'zmq_filtering': bool,

    # Connection caching. Can greatly speed up salt performance.
    'con_cache': bool,
    'rotate_aes_key': bool,

    # Cache ZeroMQ connections. Can greatly improve salt performance.
    'cache_sreqs': bool,

    # Can be set to override the python_shell=False default in the cmd module
    'cmd_safe': bool,

    # Used strictly for performance testing in RAET.
    'dummy_publisher': bool,

    # Used by salt-api for master requests timeout
    'rest_timeout': int,

    # If set, all minion exec module actions will be rerouted through sudo as this user
    'sudo_user': str,

    # HTTP request timeout in seconds. Applied for tornado http fetch functions like cp.get_url should be greater than
    # overall download time.
    'http_request_timeout': float,

    # HTTP request max file content size.
    'http_max_body': int,

    # Delay in seconds before executing bootstrap (salt cloud)
    'bootstrap_delay': int,

    # If a proxymodule has a function called 'grains', then call it during
    # regular grains loading and merge the results with the proxy's grains
    # dictionary.  Otherwise it is assumed that the module calls the grains
    # function in a custom way and returns the data elsewhere
    #
    # Default to False for 2016.3 and Carbon.  Switch to True for Nitrogen
    'proxy_merge_grains_in_module': bool,

    # Command to use to restart salt-minion
    'minion_restart_command': list,

    # Whether or not a minion should send the results of a command back to the master
    # Useful when a returner is the source of truth for a job result
    'pub_ret': bool,

    # HTTP proxy settings. Used in tornado fetch functions, apt-key etc
    'proxy_host': str,
    'proxy_username': str,
    'proxy_password': str,
    'proxy_port': int,

}
```