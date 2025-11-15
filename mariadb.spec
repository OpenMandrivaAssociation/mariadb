%define beta %{nil}
%define scmrev %{nil}
%define libmajor 18
%define muser mysql
%bcond_without pcre
%define _disable_lto 1
%global optflags %{optflags} -O2

%global __requires_exclude ^perl\\((hostnames|lib::mtr|lib::v1|mtr_|My::|wsrep)
%global __provides_exclude_from ^%{_datadir}/(mysql|mysql-test)/
#global __provides_exclude_from ^(%{_datadir}/(mysql|mysql-test)/.*|%{_libdir}/%{name}/plugin/.*\\.so)$

Summary:	The MariaDB database, a drop-in replacement for MySQL
Name:		mariadb
Version:	11.8.5
Release:	1
URL:		https://mariadb.org/
License:	GPL
Group:		System/Servers
Source0:	https://mirror.mva-n.net/mariadb//mariadb-%{version}/source/mariadb-%{version}.tar.gz
Source1:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mysql_config_multilib.sh
Source2:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/my.cnf.in
Source3:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mariadb.tmpfiles.d.in
Source4:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mysql.service.in
Source5:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mariadb-prepare-db-dir.sh
Source6:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mariadb-check-socket.sh
Source7:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mariadb-scripts-common.sh
Source8:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mariadb-check-upgrade.sh
Source9:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mysql@.service.in
Source10:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/clustercheck.sh
Source20:	mariadb.sysusers
Source1000:	%{name}.rpmlintrc
# Fedora patches
#   Patch4: Red Hat distributions specific logrotate fix
#   it would be big unexpected change, if we start shipping it now. Better wait for MariaDB 10.2
Patch4:		https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mariadb-logrotate.patch
#   Patch7: add to the CMake file all files where we want macros to be expanded
Patch7:		https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mariadb-scripts.patch
#   Patch9: pre-configure to comply with guidelines
Patch9:		https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mariadb-ownsetup.patch
#   Patch10: Fix cipher name in the SSL Cipher name test
Patch10:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mariadb-ssl-cipher-tests.patch
#   Patch11: Use PCDIR CMake option, if configured
Patch11:	https://src.fedoraproject.org/rpms/mariadb/raw/rawhide/f/mariadb-pcdir.patch

# OpenMandriva patches
# Don't strip -Wformat from --cflags -- -Werror=format-string without -Wformat
# means trouble
Patch100:	mariadb-10.0.8-fix-mysql_config.patch
# Upstream disables rocksdb on x86_32 because the build process seems to
# hang on their builders. It doesn't on ours, so let's get rid of the
# paranoia...
Patch102:	mariadb-10.3.6-enable-rocksdb-on-x86_32.patch
# wsrep is built as a library, linked to, but never installed.
# It also doesn't have soname info etc., so it should be a static
# lib
Patch103:	mariadb-10.4.4-static-wsrep.patch
# Fix libcurl detection/linkage
Patch104:	mariadb-10.9.2-fix-libcurl-detection.patch
# Make compiling great again
Patch105:	mariadb-11.7.2-compile.patch
#Patch106:	mariadb-fix-fmt-detection.patch
Requires:	%{name}-server = %{EVRD}
Requires:	%{name}-client = %{EVRD}
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	python
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemtap
BuildRequires:	libaio-devel
BuildRequires:	stdc++-devel
BuildRequires:	pkgconfig(readline)
BuildRequires:	xfsprogs-devel
BuildRequires:	pkgconfig(fmt)
BuildRequires:	pkgconfig(jemalloc)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(snappy)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(libzmq)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(msgpack-c)
BuildRequires:	pkgconfig(krb5-gssapi)
BuildRequires:	pkgconfig(com_err)
BuildRequires:	pkgconfig(libssh2)
BuildRequires:	pkgconfig(libidn2)
# For _tmpfilesdir macro
BuildRequires:	systemd-rpm-macros
BuildRequires:	cracklib-devel
BuildRequires:	pkgconfig(lzo2)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	wrap-devel
%if %{with pcre}
BuildRequires:	pkgconfig(libpcre2-8)
%endif
# For plugin/auth_pam.so
BuildRequires:	pam-devel
# For plugin/ha_oqgraph.so
BuildRequires:	boost-devel
# For JDBC plugins
%ifarch %{armx} %{ix86} %{x86_64}
BuildRequires:	jdk-current
BuildRequires:	jre-gui-current
%endif
Obsoletes:	mysql < 5.7
Provides:	mysql = 5.7

%description
The MariaDB database, a drop-in replacement for MySQL.

%define libname %mklibname mariadb 3
%define dlibname %mklibname mariadbd 19
%define oldlibname %mklibname mysqlclient %{libmajor}
%define olddlibname %mklibname mysqld 19
%if "%_lib" == "lib64"
%define archmarker ()(64bit)
%else
%define archmarker %{nil}
%endif

%package rocksdb
Summary:	RocksDB backend for MariaDB
Group:		System/Servers
Requires:	%{name} = %{EVRD}
Requires:	%{name}-server = %{EVRD}

%description rocksdb
RocksDB backend for MariaDB.

RocksDB is a high performance embedded database for key-value data.

%files rocksdb
%{_libdir}/mysql/plugin/ha_rocksdb.so
%{_bindir}/myrocks_hotbackup
%{_bindir}/mysql_ldb
%{_bindir}/mariadb-ldb
%doc %{_mandir}/man1/mariadb-ldb.1*
%{_bindir}/sst_dump
%doc %{_mandir}/man1/mysql_ldb.1*

%package -n %{libname}
Summary:	The MariaDB core library
Group:		System/Libraries
%rename %oldlibname
Provides:	libmysqlclient.so.%{libmajor}%{archmarker}
Provides:	libmysqlclient_r.so.%{libmajor}%{archmarker}

%description -n %{libname}
The MariaDB core library.

%files -n %{libname}
%{_libdir}/libmariadb.so.3
%{_libdir}/libmysqlclient.so.%{libmajor}*
%{_libdir}/libmysqlclient_r.so.%{libmajor}*

%package -n %{dlibname}
Summary:	The MariaDB daemon library
Group:		System/Libraries
%rename %olddlibname
Provides:	libmysqld.so.19%{archmarker}

%description -n %{dlibname}
The MariaDB daemon library.

%files -n %{dlibname}
%{_libdir}/libmariadbd.so.19
%{_libdir}/libmysqld.so.19

%define devpackage %mklibname -d mariadb
%define olddevpackage %mklibname -d mysqlclient

%package -n %{devpackage}
Summary:	Development files for the MariaDB database
Group:	Development/Other
Provides:	%{name}-devel = %{EVRD}
Provides:	%{mklibname -d mysqlclient_r} = %{EVRD}
Provides:	%{mklibname -d mysqld} = %{EVRD}
Requires:	%{mklibname mysqlclient 18} = %{EVRD}
Requires:	%{mklibname mysqld 19} = %{EVRD}
Requires:	%{name}-common = %{EVRD}
# Can't use -lmariadb without -lz
Requires:	pkgconfig(zlib)
Obsoletes:	%{mklibname -d mysql} < %{EVRD}
Provides:	%{mklibname -d mysql} = %{EVRD}
%rename mysql-devel
%rename %{olddevpackage}
%if "%_lib" == "lib64"
Provides:	devel(libmysqlclient(64bit))
%else
Provides:	devel(libmysqlclient)
%endif

%description -n %{devpackage}
Development files for the MariaDB database.

%files -n %{devpackage}
%{_bindir}/mariadb-config
%{_includedir}/mysql
%{_libdir}/*.so
%{_datadir}/aclocal/mysql.m4
%{_libdir}/pkgconfig/libmariadb.pc
%{_libdir}/pkgconfig/mariadb.pc
%doc %{_mandir}/man1/mariadb_config.1*
%doc %{_mandir}/man3/*.3*

%define staticpackage %mklibname -d -s mysqlclient

%package -n %{staticpackage}
Summary:	Static libraries for the MariaDB database
Requires:	%{devpackage} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}
Group:		Development/Other
Obsoletes:	mysql-static-devel < 5.7
Provides:	mysql-static-devel = 5.7

%description -n %{staticpackage}
Static libraries for the MariaDB database.

%files -n %{staticpackage}
%{_libdir}/libmysqlclient.a
%{_libdir}/libmysqlclient_r.a
%{_libdir}/libmariadb.a
%{_libdir}/libmariadbclient.a
%{_libdir}/libmariadbd.a
%{_libdir}/libmysqlservices.a

%define staticembpackage %mklibname -d -s mysqld

%package -n %{staticembpackage}
Summary:	Static libraries for the Embedded MariaDB database
Provides:	%{name}-embedded-static-devel = %{EVRD}
Group:		Development/Other
Requires:	%{staticpackage} = %{EVRD}

%description -n %{staticembpackage}
Static libraries for the Embedded MariaDB database.

%files -n %{staticembpackage}
%{_libdir}/libmysqld.a

%package plugin
Summary:	MariaDB plugins
Group:		Databases
Obsoletes:	mysql-plugin < 5.7
Provides:	mysql-plugin = 5.7
Conflicts:	mysql-server <= 5.5.30-3

%description plugin
Plugins for the MariaDB database.

%files plugin
%{_libdir}/mysql/plugin/adt_null.so
%{_libdir}/mysql/plugin/auth_0x0100.so
%{_libdir}/mysql/plugin/auth_ed25519.so
%{_libdir}/mysql/plugin/auth_gssapi.so
%{_libdir}/mysql/plugin/auth_gssapi_client.so
%{_libdir}/mysql/plugin/auth_mysql_sha2.so
%{_libdir}/mysql/plugin/auth_test_plugin.so
%{_libdir}/mysql/plugin/auth_pam.so
%{_libdir}/mysql/plugin/auth_parsec.so
# Change from root:root to mysql:mysql, so it can be accessed by the server
%attr(0755,mysql,mysql) %dir %{_libdir}/mysql/plugin/auth_pam_tool_dir
%{_libdir}/mysql/plugin/auth_pam_tool_dir/auth_pam_tool
%{_libdir}/mysql/plugin/auth_pam_v1.so
%{_libdir}/mysql/plugin/caching_sha2_password.so
%{_libdir}/mysql/plugin/client_ed25519.so
%{_libdir}/mysql/plugin/cracklib_password_check.so
%{_libdir}/mysql/plugin/daemon_example.ini
%{_libdir}/mysql/plugin/dialog.so
%{_libdir}/mysql/plugin/dialog_examples.so
%{_libdir}/mysql/plugin/disks.so
%{_libdir}/mysql/plugin/ha_archive.so
%{_libdir}/mysql/plugin/ha_blackhole.so
%{_libdir}/mysql/plugin/ha_connect.so
%{_libdir}/mysql/plugin/ha_example.so
%{_libdir}/mysql/plugin/ha_federated.so
%{_libdir}/mysql/plugin/ha_federatedx.so
%{_libdir}/mysql/plugin/ha_sphinx.so
%{_libdir}/mysql/plugin/ha_spider.so
%{_libdir}/mysql/plugin/ha_test_sql_discovery.so
%{_libdir}/mysql/plugin/ha_mroonga.so
%{_libdir}/mysql/plugin/handlersocket.so
%{_libdir}/mysql/plugin/libdaemon_example.so
%{_libdir}/mysql/plugin/locales.so
%{_libdir}/mysql/plugin/metadata_lock_info.so
%{_libdir}/mysql/plugin/mypluglib.so
%{_libdir}/mysql/plugin/mysql_clear_password.so
%{_libdir}/mysql/plugin/parsec.so
%{_libdir}/mysql/plugin/qa_auth_client.so
%{_libdir}/mysql/plugin/qa_auth_interface.so
%{_libdir}/mysql/plugin/qa_auth_server.so
%{_libdir}/mysql/plugin/query_cache_info.so
%{_libdir}/mysql/plugin/query_response_time.so
%{_libdir}/mysql/plugin/server_audit.so
%{_libdir}/mysql/plugin/sha256_password.so
%{_libdir}/mysql/plugin/sql_errlog.so
%{_libdir}/mysql/plugin/test_versioning.so
%{_libdir}/mysql/plugin/password_reuse_check.so
%{_libdir}/mysql/plugin/provider_bzip2.so
%{_libdir}/mysql/plugin/provider_lz4.so
%{_libdir}/mysql/plugin/provider_lzma.so
%{_libdir}/mysql/plugin/provider_lzo.so
%{_libdir}/mysql/plugin/provider_snappy.so
%{_libdir}/mysql/plugin/hashicorp_key_management.so
%{_libdir}/mysql/plugin/zstd.so
%doc %{_mandir}/man1/mysql_plugin.1*
%{_libdir}/mysql/plugin/debug_key_management.so
%{_libdir}/mysql/plugin/example_key_management.so
%{_libdir}/mysql/plugin/file_key_management.so
%{_libdir}/mysql/plugin/simple_password_check.so
%{_libdir}/mysql/plugin/wsrep_info.so
#ifarch %{armx} x86_64 %{ix86} znver1
#{_datadir}/mysql/JavaWrappers.jar
#endif
%optional %{_datadir}/mysql/JdbcInterface.jar
%optional %{_datadir}/mysql/Mongo2.jar
%optional %{_datadir}/mysql/Mongo3.jar

%package test
Summary:	MariaDB test suite
Group:		System/Servers
Obsoletes:	mysql-test < 5.7
Provides:	mysql-test = 5.7

%description test
MariaDB test suite.

%files test
%{_bindir}/mysqltest
%{_bindir}/mysqltest_embedded
%{_bindir}/mariadb-client-test-embedded
%doc %{_mandir}/man1/mariadb-client-test-embedded.1*
%{_bindir}/mariadb-test
%{_bindir}/mariadb-test-embedded
%doc %{_mandir}/man1/mariadb-test-embedded.1*
%{_bindir}/mysql_client_test
%{_bindir}/mariadb-client-test
%doc %{_mandir}/man1/mariadb-client-test.1*
%{_bindir}/mysql_client_test_embedded
%{_datadir}/mysql-test
%{_datadir}/mysql/mini-benchmark
%{_libdir}/mysql/plugin/func_test.so
%{_libdir}/mysql/plugin/type_test.so
%doc %{_mandir}/man1/mariadb-test.1*
%doc %{_mandir}/man1/mysql-stress-test.pl.1*
%doc %{_mandir}/man1/mysql-test-run.pl.1*
%doc %{_mandir}/man1/mysql_client_test.1*
%doc %{_mandir}/man1/mysql_client_test_embedded.1*
%doc %{_mandir}/man1/mysqltest.1*
%doc %{_mandir}/man1/mysqltest_embedded.1*

%package server
Summary:	MariaDB server
Group:		System/Servers
Requires:	%{name}-common = %{EVRD}
Requires:	%{name}-plugin = %{EVRD}
Obsoletes:	mysql-server < 5.7
Provides:	mysql-server = 5.7
%systemd_requires
Requires(pre):	systemd
Suggests:	%{name}-rocksdb = %{EVRD}

%description server
The MariaDB server. For a full MariaDB database server, install
package '%{name}'.

%pre server
%sysusers_create_package %{name} %{SOURCE20}

%files server
%optional %{_libdir}/mysql/plugin/ha_s3.so
%{_libdir}/mysql/plugin/test_sql_service.so
%{_libdir}/mysql/plugin/type_mysql_json.so
%{_libdir}/mysql/plugin/type_mysql_timestamp.so
%doc %{_mandir}/man1/aria_s3_copy.1*
%doc %{_mandir}/man1/mariadb-conv.1*
%doc %{_mandir}/man1/myrocks_hotbackup.1*
%doc %{_mandir}/man1/mytop.1*
%{_sysconfdir}/security/user_map.conf
/%{_lib}/security/pam_user_map.so
%optional %{_bindir}/aria_s3_copy
%{_bindir}/mariabackup
%{_bindir}/mariadb-backup
%{_bindir}/mariadb-conv
%doc %{_mandir}/man1/mariadb-backup.1*
%{_bindir}/mbstream
%dir %{_datadir}/mysql
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mariadb_performance_tables.sql
%{_datadir}/mysql/mariadb_system_tables.sql
%{_datadir}/mysql/mariadb_system_tables_data.sql
%{_datadir}/mysql/mariadb_test_data_timezone.sql
%{_datadir}/mysql/wsrep_notify
%{_datadir}/mysql/*.cnf
%{_datadir}/mysql/maria_add_gis_sp.sql
%{_datadir}/mysql/maria_add_gis_sp_bootstrap.sql
%{_datadir}/mysql/mroonga
%{_datadir}/groonga
%{_datadir}/groonga-normalizer-mysql
%{_sysusersdir}/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%doc %{_mandir}/man1/mariabackup.1*
%doc %{_mandir}/man1/mbstream.1*
%doc %{_mandir}/man8/*
%dir %{_libdir}/mysql
%dir %{_libdir}/mysql/plugin
%{_sysconfdir}/logrotate.d/mariadb
%{_datadir}/mysql/mariadb.logrotate
%config(noreplace) %{_sysconfdir}/my.cnf.d/client.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/mysql-clients.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/server.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/enable_encryption.preset
%{_bindir}/aria_chk
%{_bindir}/aria_dump_log
%{_bindir}/aria_ftdump
%{_bindir}/aria_pack
%{_bindir}/aria_read_log
%{_bindir}/galera_new_cluster
%{_bindir}/galera_recovery
%{_bindir}/innochecksum
%{_bindir}/myisam_ftdump
%{_bindir}/myisamchk
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_convert_table_format
%{_bindir}/mariadb-convert-table-format
%doc %{_mandir}/man1/mariadb-convert-table-format.1*
%{_bindir}/mysql_fix_extensions
%{_bindir}/mariadb-fix-extensions
%doc %{_mandir}/man1/mariadb-fix-extensions.1*
%{_bindir}/mysql_install_db
%{_bindir}/mariadb-install-db
%doc %{_mandir}/man1/mariadb-install-db.1*
%{_bindir}/mysql_plugin
%{_bindir}/mariadb-plugin
%doc %{_mandir}/man1/mariadb-plugin.1*
%{_bindir}/mysql_secure_installation
%{_bindir}/mariadb-secure-installation
%doc %{_mandir}/man1/mariadb-secure-installation.1*
%{_bindir}/mysql_setpermission
%{_bindir}/mariadb-setpermission
%doc %{_mandir}/man1/mariadb-setpermission.1*
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mariadb-tzinfo-to-sql
%doc %{_mandir}/man1/mariadb-tzinfo-to-sql.1*
%{_bindir}/mysql_upgrade
%doc %{_mandir}/man1/mariadb-upgrade.1*
%{_bindir}/mariadb-upgrade
%{_bindir}/mysqld_multi
%{_bindir}/mariadbd-multi
%doc %{_mandir}/man1/mariadbd-multi.1*
%{_bindir}/mysqld_safe
%{_bindir}/mariadbd-safe
%doc %{_mandir}/man1/mariadbd-safe.1*
%{_bindir}/mysqld_safe_helper
%{_bindir}/mariadbd-safe-helper
%doc %{_mandir}/man1/mariadbd-safe-helper.1*
%{_bindir}/mysqlhotcopy
%{_bindir}/mariadb-hotcopy
%doc %{_mandir}/man1/mariadb-hotcopy.1*
%{_bindir}/mytop
%{_bindir}/perror
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip
%{_bindir}/wsrep_*
%{_sbindir}/mysqld
%{_sbindir}/mariadbd
%{_bindir}/mariadb
%doc %{_mandir}/man1/mariadb.1*
%{_bindir}/mariadb-service-convert
%{_sbindir}/mariadb-prepare-db-dir
%{_sbindir}/mariadb-check-socket
%{_sbindir}/mariadb-check-upgrade
%{_sbindir}/mariadb-scripts-common
%{_unitdir}/*.service
%{_unitdir}/*.socket
%dir %{_unitdir}/mariadb@bootstrap.service.d
%{_unitdir}/mariadb@bootstrap.service.d/*.conf
%{_datadir}/mysql/mariadb_test_db.sql
%doc %{_docdir}/%{name}-%{version}
%attr(711,%{muser},%{muser}) /srv/mysql
%attr(711,%{muser},%{muser}) %{_localstatedir}/log/mysqld
%doc %{_mandir}/man1/aria_chk.1*
%doc %{_mandir}/man1/aria_dump_log.1*
%doc %{_mandir}/man1/aria_ftdump.1*
%doc %{_mandir}/man1/aria_pack.1*
%doc %{_mandir}/man1/aria_read_log.1*
%doc %{_mandir}/man1/galera_new_cluster.1*
%doc %{_mandir}/man1/galera_recovery.1*
%doc %{_mandir}/man1/innochecksum.1*
%doc %{_mandir}/man1/mariadb-service-convert.1*
%doc %{_mandir}/man1/myisam_ftdump.1*
%doc %{_mandir}/man1/myisamchk.1*
%doc %{_mandir}/man1/myisamlog.1*
%doc %{_mandir}/man1/myisampack.1*
%doc %{_mandir}/man1/mysql.server.1*
%doc %{_mandir}/man1/mysql_config.1*
%doc %{_mandir}/man1/mysql_convert_table_format.1*
%doc %{_mandir}/man1/mysql_fix_extensions.1*
%doc %{_mandir}/man1/mysql_install_db.1*
%doc %{_mandir}/man1/mysql_secure_installation.1*
%doc %{_mandir}/man1/mysql_setpermission.1*
%doc %{_mandir}/man1/mysql_tzinfo_to_sql.1*
%doc %{_mandir}/man1/mysql_upgrade.1*
%doc %{_mandir}/man1/mysqld_multi.1*
%doc %{_mandir}/man1/my_safe_process.1*
%doc %{_mandir}/man1/mysqld_safe.1*
%doc %{_mandir}/man1/mysqld_safe_helper.1*
%doc %{_mandir}/man1/mysqlhotcopy.1*
%doc %{_mandir}/man1/perror.1*
%doc %{_mandir}/man1/replace.1*
%doc %{_mandir}/man1/resolve_stack_dump.1*
%doc %{_mandir}/man1/resolveip.1*
%doc %{_mandir}/man1/wsrep_sst_common.1*
%doc %{_mandir}/man1/wsrep_sst_mysqldump.1*
%doc %{_mandir}/man1/wsrep_sst_rsync.1*
%doc %{_mandir}/man1/wsrep_sst_mariabackup.1*
%doc %{_mandir}/man1/wsrep_sst_rsync_wan.1*
%doc %{_mandir}/man1/wsrep_sst_backup.1.zst

%{_datadir}/mysql/mariadb_sys_schema.sql

%package msql2mysql
Summary:	Tool to convert code written for mSQL to MySQL/MariaDB
Group:		Development/Other

%description msql2mysql
Tool to convert code written for mSQL to MySQL/MariaDB.

%files msql2mysql
%{_bindir}/msql2mysql
%doc %{_mandir}/man1/msql2mysql.1*

%package common
Summary:	Common files needed by both the MariaDB server and client
Group:		System/Servers
Obsoletes:	mysql-common < 5.7
Provides:	mysql-common = 5.7
Requires:	%{name}-common-binaries = %{EVRD}
Requires:	%{name}-client = %{EVRD}

%description common
Common files needed by both the MariaDB server and client.

%files common
%doc COPYING
%config(noreplace) %{_sysconfdir}/my.cnf
%dir %{_sysconfdir}/my.cnf.d
%dir %{_datadir}/mysql
%{_sysconfdir}/my.cnf.d/*
%{_datadir}/mysql/english
%{_datadir}/mysql/charsets
%{_datadir}/mysql/bulgarian
%{_datadir}/mysql/chinese
%{_datadir}/mysql/czech
%{_datadir}/mysql/danish
%{_datadir}/mysql/dutch
%{_datadir}/mysql/estonian
%{_datadir}/mysql/french
%{_datadir}/mysql/georgian
%{_datadir}/mysql/german
%{_datadir}/mysql/greek
%{_datadir}/mysql/hindi
%{_datadir}/mysql/hungarian
%{_datadir}/mysql/italian
%{_datadir}/mysql/japanese
%{_datadir}/mysql/korean
%{_datadir}/mysql/norwegian
%{_datadir}/mysql/norwegian-ny
%{_datadir}/mysql/polish
%{_datadir}/mysql/portuguese
%{_datadir}/mysql/romanian
%{_datadir}/mysql/russian
%{_datadir}/mysql/serbian
%{_datadir}/mysql/slovak
%{_datadir}/mysql/spanish
%{_datadir}/mysql/swahili
%{_datadir}/mysql/swedish
%{_datadir}/mysql/ukrainian
%{_datadir}/mysql/policy
# We put this into -common for now because it is needed for both
# -server (used by mysqld_safe) and by -devel (configure scripts calling
# it, e.g. php)
%{_bindir}/mariadb_config
%{_bindir}/mysql_config

%package common-binaries
Summary:	Common binary files needed by both the MariaDB server and client
Group:		System/Servers
Obsoletes:	mysql-common < 5.7
Provides:	mysql-common = 5.7
Requires:	%{name}-common = %{EVRD}

%description common-binaries
Common files needed by both the MariaDB server and client.

%files common-binaries
%{_bindir}/my_print_defaults
%doc %{_mandir}/man1/my_print_defaults.1*

%package client
Summary:	MariaDB command line client
Group:		Databases
Obsoletes:	mysql-client < 5.7
Provides:	mysql-client = 5.7
Conflicts:	mysql-server <= 5.5.30-3

%description client
MariaDB command line client.

%files client
%{_bindir}/mysql
%{_bindir}/mysql_embedded
%{_bindir}/mariadb-embedded
%doc %{_mandir}/man1/mariadb-embedded.1*
%doc %{_mandir}/man1/mysql_embedded.1*
%{_bindir}/mysqlaccess
%{_bindir}/mariadb-access
%doc %{_mandir}/man1/mariadb-access.1*
%{_bindir}/mysqladmin
%{_bindir}/mariadb-admin
%doc %{_mandir}/man1/mariadb-admin.1*
%{_bindir}/mysqlbinlog
%{_bindir}/mariadb-binlog
%doc %{_mandir}/man1/mariadb-binlog.1*
%{_bindir}/mysqlcheck
%{_bindir}/mariadb-check
%doc %{_mandir}/man1/mariadb-check.1*
%{_bindir}/mysqldump
%{_bindir}/mariadb-dump
%doc %{_mandir}/man1/mariadb-dump.1*
%{_bindir}/mysqldumpslow
%{_bindir}/mariadb-dumpslow
%doc %{_mandir}/man1/mariadb-dumpslow.1*
%{_bindir}/mysql_find_rows
%{_bindir}/mariadb-find-rows
%doc %{_mandir}/man1/mariadb-find-rows.1*
%{_bindir}/mysqlimport
%{_bindir}/mariadb-import
%doc %{_mandir}/man1/mariadb-import.1*
%{_bindir}/mysqlshow
%{_bindir}/mariadb-show
%doc %{_mandir}/man1/mariadb-show.1*
%{_bindir}/mysqlslap
%{_bindir}/mariadb-slap
%doc %{_mandir}/man1/mariadb-slap.1*
%{_bindir}/mysql_waitpid
%doc %{_mandir}/man1/mariadb-waitpid.1*
%{_bindir}/mariadb-waitpid
%{_bindir}/test-connect-t
%doc %{_mandir}/man1/mysql.1*
%doc %{_mandir}/man1/mysqlaccess.1*
%doc %{_mandir}/man1/mysqladmin.1*
%doc %{_mandir}/man1/mysqlbinlog.1*
%doc %{_mandir}/man1/mysqlcheck.1*
%doc %{_mandir}/man1/mysqldump.1*
%doc %{_mandir}/man1/mysqldumpslow.1*
%doc %{_mandir}/man1/mysql_find_rows.1*
%doc %{_mandir}/man1/mysqlimport.1*
%doc %{_mandir}/man1/mysqlslap.1*
%doc %{_mandir}/man1/mysqlshow.1*
%doc %{_mandir}/man1/mysql_waitpid.1*

%prep
%autosetup -p1
# MariaDB uses python2 scripts to autogenerate some sources...
# Let's use python3 instead.
#find . -name "*.py" |xargs 2to3 -w

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} %{SOURCE10} scripts

# Workarounds for bugs
sed -i "s@data/test@\${INSTALL_MYSQLTESTDIR}@g" sql/CMakeLists.txt
#sed -i "s/srv_buf_size/srv_sort_buf_size/" storage/innobase/row/row0log.cc

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="%{optflags} -fno-strict-aliasing"
%ifarch %{riscv64}
export CXXFLAGS="%{optflags} -fno-strict-aliasing -latomic"
%endif

[ -e %{_sysconfdir}/profile.d/90java.sh ] && . %{_sysconfdir}/profile.d/90java.sh

%ifarch riscv64 %{ix86}
# clang 8.0.1-0.359209.1 on x86_32
# needs an extra -latomic for rocksdblib
export CC=gcc
export CXX=g++
%else
export CC="%{__cc} -Wno-unknown-warning-option -Wno-extern-c-compat -Qunused-arguments"
export CXX="%{__cxx} -Wno-unknown-warning-option -Wno-extern-c-compat -Qunused-arguments"
export CFLAGS="$CFLAGS -Wno-error=pointer-bool-conversion -Wno-error=missing-field-initializers"
export CXXFLAGS="$CFLAGS -Wno-error=pointer-bool-conversion -Wno-error=missing-field-initializers -fcxx-exceptions"
%endif

if echo $CC |grep -q gcc; then
    export CFLAGS="$CFLAGS -Wno-error=maybe-uninitialized"
    export CXXFLAGS="$CXXFLAGS -Wno-error=maybe-uninitialized"
fi
export LDFLAGS="$LDFLAGS -fuse-ld=bfd"

# (tpg) install services into %_unitdir
sed -i -e "s,/usr/lib/systemd/system,%{_unitdir},g" cmake/install_layout.cmake

# (tpg) fix error: 'noreturn' attribute only applies to functions
sed -i 's|WSREP_NORETURN|__attribute__((noreturn))|' wsrep-lib/include/wsrep/thread_service.hpp

# DISABLE_LIBMYSQLCLIENT_SYMBOL_VERSIONING breaks binary compatibility
# with some other distributions, but fixes the loading
# of the Qt mysql plugin. Better fix wanted.

%cmake	-DBUILD_CONFIG=mysql_release \
	-DINSTALL_LAYOUT=RPM \
	-DFEATURE_SET="community" \
	-DWITH_SSL=system \
	-DWITH_ZLIB=system \
	-DWITH_FMT=system \
%if %{with pcre}
	-DWITH_PCRE=system \
%endif
	-DDISABLE_LIBMYSQLCLIENT_SYMBOL_VERSIONING:BOOL=ON \
	-DINSTALL_SYSCONFDIR="%{_sysconfdir}" \
	-DINSTALL_SYSCONF2DIR="%{_sysconfdir}/my.cnf.d" \
	-DINSTALL_DOCDIR="share/doc/%{_pkgdocdirname}" \
	-DINSTALL_DOCREADMEDIR="share/doc/%{_pkgdocdirname}" \
	-DINSTALL_INCLUDEDIR=include/mysql \
	-DINSTALL_INFODIR=share/info \
	-DINSTALL_LIBDIR="%{_lib}" \
	-DINSTALL_MANDIR=share/man \
	-DINSTALL_MYSQLSHAREDIR=share/mysql \
	-DINSTALL_MYSQLTESTDIR=share/mysql-test \
	-DINSTALL_PLUGINDIR="%{_lib}/mysql/plugin" \
	-DINSTALL_SBINDIR=bin \
	-DINSTALL_SCRIPTDIR=bin \
	-DINSTALL_SUPPORTFILESDIR=share/mysql \
	-DINSTALL_PCDIR=%{_lib}/pkgconfig \
	-DINSTALL_PLUGINDIR="%{_lib}/mysql/plugin" \
	-DINSTALL_LIBDIR="%{_libdir}" \
	-DMYSQL_DATADIR=/srv/mysql \
	-DMYSQL_UNIX_ADDR=/run/mysqld/mysql.sock \
	-DPID_FILE_DIR="/run/mysqld" \
	-DWITH_EXTRA_CHARSETS=complex \
	-DWITH_EMBEDDED_SERVER:BOOL=ON \
	-DWITH_READLINE:BOOL=ON \
	-DWITH_LIBEVENT=system \
	-DINSTALL_SYSTEMD_unitdir_RPM="%{_unitdir}" \
	-DCOMPILATION_COMMENT="%{_vendor} MariaDB Server" \
	-DCONC_WITH_CURL:BOOL=ON \
	-DCONC_WITH_SSL:BOOL=ON \
	-DLOAD_LOCAL_INFILE:BOOL=ON \
	-DLZ4_LIBS=%{_libdir}/liblz4.so \
	-DWITH_MYSQLCOMPAT:BOOL=ON \
	-DWITH_WSREP:BOOL=ON \
	-DWITH_EMBEDDED_SERVER:BOOL=ON \
	-DWITH_MARIABACKUP:BOOL=ON \
	-DPLUGIN_ROCKSDB=DYNAMIC \
	-DCURL_LIBRARIES=-lcurl

%make_build -k || make

%install
%make_install -C build

# systemd integration
rm -rf %{buildroot}%{_sysconfdir}/init.d
install -D -p -m 0644 build/scripts/mariadb.tmpfiles.d %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -D -p -m 0644 %{SOURCE20} %{buildroot}%{_sysusersdir}/%{name}.conf

# Remove upstream SysV init script and a symlink to that, we use systemd
rm %{buildroot}%{_sbindir}/rcmysql
rm -r %{buildroot}%{_datadir}/mysql/systemd
# Our downstream Systemd service file have set aliases to the "mysql" names in the [Install] section.
# They can be enabled / disabled by "systemctl enable / diable <service_name>"
rm %{buildroot}%{_unitdir}/{mysql,mysqld}.service
 
# install systemd unit files and scripts for handling server startup
install -D -p -m 644 build/scripts/mysql.service %{buildroot}%{_unitdir}/mariadb.service
install -D -p -m 644 build/scripts/mysql@.service %{buildroot}%{_unitdir}/mariadb@.service

# helper scripts for service starting
install -D -p -m 755 build/scripts/mariadb-prepare-db-dir %{buildroot}%{_sbindir}/mariadb-prepare-db-dir
install -p -m 755 build/scripts/mariadb-check-socket %{buildroot}%{_sbindir}/mariadb-check-socket
install -p -m 755 build/scripts/mariadb-check-upgrade %{buildroot}%{_sbindir}/mariadb-check-upgrade
install -p -m 644 build/scripts/mariadb-scripts-common %{buildroot}%{_sbindir}/mariadb-scripts-common

# Fix bogus doc installation
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
find %{buildroot}%{_docdir} -type f -exec mv {} %{buildroot}%{_docdir}/%{name}-%{version}/ ';'

mkdir -p %{buildroot}/srv/mysql \
	%{buildroot}%{_localstatedir}/log/mysqld
chmod 711 %{buildroot}/srv/mysql \
	%{buildroot}%{_localstatedir}/log/mysqld

# Unneeded stuff
rm -f	%{buildroot}%{_datadir}/mysql/binary-configure \
	%{buildroot}%{_datadir}/mysql/magic \
	%{buildroot}%{_datadir}/mysql/mysql-log-rotate \
	%{buildroot}%{_datadir}/mysql/solaris/postinstall-solaris
# Should those go to docs rather than just being deleted?
rm -f	%{buildroot}%{_datadir}/mysql/config.huge.ini \
	%{buildroot}%{_datadir}/mysql/config.medium.ini \
	%{buildroot}%{_datadir}/mysql/config.small.ini \
	%{buildroot}%{_datadir}/mysql/mysql.server \
	%{buildroot}%{_datadir}/mysql/mysqld_multi.server \
	%{buildroot}%{_datadir}/mysql/ndb-config-2-node.ini \
	%{buildroot}%{_datadir}/mysql/SELinux/RHEL4/mysql.fc \
	%{buildroot}%{_datadir}/mysql/SELinux/RHEL4/mysql.te

# for compatibility
ln -s libmariadb.so.3 %{buildroot}%{_libdir}/libmysqlclient_r.so.18
ln -s libmariadb.so.3 %{buildroot}%{_libdir}/libmysqlclient.so.18
ln -s libmariadb.so.3 %{buildroot}%{_libdir}/libmysqld.so.19

%ifarch riscv64
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
mv %{buildroot}/usr/lib/pkgconfig/libmariadb.pc %{buildroot}/%{_libdir}/pkgconfig/
rm -rf %{buildroot}/usr/lib/pkgconfig/
%endif

%files
# meta package
