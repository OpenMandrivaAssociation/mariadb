%define beta %{nil}
%define scmrev %{nil}
%define libmajor 18
%define muser mysql

Name: mariadb
Version: 10.0.7
Release: 1
Source0: http://mirrors.fe.up.pt/pub/mariadb/mariadb-%{version}/kvm-tarbake-jaunty-x86/mariadb-%{version}.tar.gz
Source100: mysqld.service
Source101: mysqld-prepare-db-dir
Source102: mysqld-wait-ready
Source1000: %{name}.rpmlintrc
Summary: The MariaDB database, a drop-in replacement for MySQL
URL: http://mariadb.org/
License: GPL
Group: System/Servers
Requires: %{name}-server = %{EVRD}
Requires: %{name}-client = %{EVRD}
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	python
BuildRequires:	systemd-units
BuildRequires:	systemtap
BuildRequires:	libaio-devel
BuildRequires:	stdc++-devel
BuildRequires:	readline-devel
BuildRequires:	xfsprogs-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	wrap-devel
# For plugin/auth_pam.so
BuildRequires:	pam-devel
# For plugin/ha_oqgraph.so
BuildRequires:	boost-devel

%description
The MariaDB database, a drop-in replacement for MySQL

%libpackage mysqlclient %{libmajor}
%{_libdir}/libmysqlclient_r.so.%{libmajor}*

%define devpackage %mklibname -d mysqlclient

%package -n %{devpackage}
Summary: Development files for the MariaDB database
Provides: %{name}-devel = %{EVRD}
Provides: %{mklibname -d mysqlclient_r} = %{EVRD}
Requires: %{mklibname mysqlclient 18} = %{EVRD}
Obsoletes: %{mklibname -d mysql} < %{EVRD}
Provides: %{mklibname -d mysql} = %{EVRD}
%rename mysql-devel
Group: Development/Other

%description -n %{devpackage}
Development files for the MariaDB database

%files -n %{devpackage}
%{_includedir}/mysql
%{_libdir}/*.so
%{_datadir}/aclocal/mysql.m4

%define staticpackage %mklibname -d -s mysqlclient

%package -n %{staticpackage}
Summary: Static libraries for the MariaDB database
Provides: %{name}-static-devel = %{EVRD}
Group: Development/Other

%description -n %{staticpackage}
Static libraries for the MariaDB database

%files -n %{staticpackage}
%{_libdir}/libmysqlclient.a
%{_libdir}/libmysqlclient_r.a
%{_libdir}/libmysqlservices.a

%package plugin
Summary: MariaDB plugins
Group: Databases

%description plugin
Plugins for the MariaDB database

%files plugin
%{_libdir}/mysql/plugin/adt_null.so
%{_libdir}/mysql/plugin/auth_0x0100.so
%{_libdir}/mysql/plugin/auth_pam.so
%{_libdir}/mysql/plugin/auth_socket.so
%{_libdir}/mysql/plugin/auth_test_plugin.so
%{_libdir}/mysql/plugin/daemon_example.ini
%{_libdir}/mysql/plugin/dialog.so
%{_libdir}/mysql/plugin/dialog_examples.so
%{_libdir}/mysql/plugin/feedback.so
%{_libdir}/mysql/plugin/ha_archive.so
%{_libdir}/mysql/plugin/ha_blackhole.so
%{_libdir}/mysql/plugin/ha_connect.so
%{_libdir}/mysql/plugin/ha_example.so
%{_libdir}/mysql/plugin/ha_federated.so
%{_libdir}/mysql/plugin/ha_federatedx.so
%{_libdir}/mysql/plugin/ha_sequence.so
%{_libdir}/mysql/plugin/ha_sphinx.so
%{_libdir}/mysql/plugin/ha_spider.so
%{_libdir}/mysql/plugin/ha_test_sql_discovery.so
%{_libdir}/mysql/plugin/ha_xtradb.so
%{_libdir}/mysql/plugin/handlersocket.so
%{_libdir}/mysql/plugin/libdaemon_example.so
%{_libdir}/mysql/plugin/locales.so
%{_libdir}/mysql/plugin/metadata_lock_info.so
%{_libdir}/mysql/plugin/mypluglib.so
%{_libdir}/mysql/plugin/mysql_clear_password.so
%{_libdir}/mysql/plugin/qa_auth_client.so
%{_libdir}/mysql/plugin/qa_auth_interface.so
%{_libdir}/mysql/plugin/qa_auth_server.so
%{_libdir}/mysql/plugin/query_cache_info.so
%{_libdir}/mysql/plugin/query_response_time.so
%{_libdir}/mysql/plugin/sphinx.so
%{_libdir}/mysql/plugin/semisync_master.so
%{_libdir}/mysql/plugin/semisync_slave.so
%{_libdir}/mysql/plugin/sql_errlog.so
%{_mandir}/man1/mysql_plugin.1*

%package plugin-tokudb
Summary: The TokuDB storage engine plugin for MariaDB
Requires: %{name}-server = %{EVRD}
Group: Databases

%description plugin-tokudb
The TokuDB storage engine plugin for MariaDB.

TokuDB is a storage engine for MySQL and MariaDB that is specifically
designed for high performance on write-intensive workloads.
It achieves this via Fractal Tree indexing. TokuDB is a scalable, ACID
and MVCC compliant storage engine that provides indexing-based query
improvements, offers online schema modifications, and reduces slave lag
for both hard disk drives and flash memory.

# As of 10.0.6, tokudb is x86_64 only
%ifarch x86_64
%files plugin-tokudb
%{_libdir}/mysql/plugin/ha_tokudb.so
%{_sysconfdir}/my.cnf.d/tokudb.cnf
%{_bindir}/tokuftdump
%endif

%package test
Summary: MariaDB test suite
Group: System/Servers

%description test
MariaDB test suite

%files test
%{_bindir}/mysqltest
%{_bindir}/mysql_client_test
%{_datadir}/mysql-test
%{_mandir}/man1/mysql-stress-test.pl.1*
%{_mandir}/man1/mysql-test-run.pl.1*
%{_mandir}/man1/mysql_client_test.1*
%{_mandir}/man1/mysql_client_test_embedded.1*
%{_mandir}/man1/mysqltest.1*
%{_mandir}/man1/mysqltest_embedded.1*

%package server
Summary: MariaDB server
Group: System/Servers
Requires: %{name}-common = %{EVRD}
Requires: %{name}-plugin = %{EVRD}

%description server
The MariaDB server. For a full MariaDB database server, install
package '%{name}'.

%pre server
%_pre_useradd %{muser} /srv/mysql /sbin/nologin

%post server
%_post_service mysqld mysqld.service

%preun server
%_preun_service mysqld mysqld.service

%files server
%dir %{_datadir}/mysql
%{_datadir}/mysql/errmsg-utf8.txt
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/install_spider.sql
%{_datadir}/mysql/mysql_performance_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/*.cnf
%{_mandir}/man8/*
%dir %{_libdir}/mysql
%dir %{_libdir}/mysql/plugin
%{_sysconfdir}/logrotate.d/mysql
%{_sysconfdir}/my.cnf.d/client.cnf
%{_sysconfdir}/my.cnf.d/mysql-clients.cnf
%{_sysconfdir}/my.cnf.d/server.cnf
%{_bindir}/aria_chk
%{_bindir}/aria_dump_log
%{_bindir}/aria_ftdump
%{_bindir}/aria_pack
%{_bindir}/aria_read_log
%{_bindir}/innochecksum
%{_bindir}/myisam_ftdump
%{_bindir}/myisamchk
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_install_db
%{_bindir}/mysql_plugin
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_setpermission
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysql_upgrade
%{_bindir}/mysql_zap
%{_bindir}/mysqlbug
%{_bindir}/mysqld_multi
%{_bindir}/mysqld_safe
%{_bindir}/mysqlhotcopy
%{_bindir}/mytop
%{_bindir}/perror
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip
%{_sbindir}/mysqld
/lib/systemd/system/mysqld.service
%{_bindir}/mysqld-prepare-db-dir
%{_bindir}/mysqld-wait-ready
%doc %{_docdir}/%{name}-%{version}
%attr(711,%{muser},%{muser}) /srv/mysql
%attr(711,%{muser},%{muser}) %{_localstatedir}/log/mysqld
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_config.1*
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysql_fix_privilege_tables.1*
%{_mandir}/man1/mysql_install_db.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_setpermission.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqlbug.1*
%{_mandir}/man1/mysqld_multi.1*
%{_mandir}/man1/mysqld_safe.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysqlman.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolve_stack_dump.1*
%{_mandir}/man1/resolveip.1*

%package msql2mysql
Summary: Tool to convert code written for mSQL to MySQL/MariaDB
Group: Development/Other

%description msql2mysql
Tool to convert code written for mSQL to MySQL/MariaDB

%files msql2mysql
%{_bindir}/msql2mysql
%{_mandir}/man1/msql2mysql.1*

%package common
Summary: Common files needed by both the MariaDB server and client
Group: System/Servers
BuildArch: noarch

%description common
Common files needed by both the MariaDB server and client

%files common
%doc README COPYING
%{_sysconfdir}/my.cnf
%dir %{_sysconfdir}/my.cnf.d
%dir %{_datadir}/mysql
%{_datadir}/mysql/english
%{_datadir}/mysql/charsets
%{_datadir}/mysql/czech
%{_datadir}/mysql/danish
%{_datadir}/mysql/dutch
%{_datadir}/mysql/estonian
%{_datadir}/mysql/french
%{_datadir}/mysql/german
%{_datadir}/mysql/greek
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
%{_datadir}/mysql/swedish
%{_datadir}/mysql/ukrainian
# We put this into -common for now because it is needed for both
# -server (used by mysqld_safe) and by -devel (configure scripts calling
# it, e.g. php)
%{_bindir}/mysql_config

%package client
Summary: MariaDB command line client
Group: Databases

%description client
MariaDB command line client

%files client
%{_bindir}/mysql
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{_bindir}/mysqldumpslow
%{_bindir}/mysql_find_rows
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap
%{_bindir}/mysql_waitpid
%{_bindir}/my_print_defaults
%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlslap.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysql_waitpid.1*
%{_mandir}/man1/my_print_defaults.1*

%prep
%setup -q
# Workarounds for bugs
sed -i "s@data/test@\${INSTALL_MYSQLTESTDIR}@g" sql/CMakeLists.txt
#sed -i "s/srv_buf_size/srv_sort_buf_size/" storage/innobase/row/row0log.cc
sed -i 's, -fuse-linker-plugin,,' storage/tokudb/ft-index/cmake_modules/TokuSetupCompiler.cmake storage/tokudb/CMakeLists.txt

# aliasing rule violations at least in storage/tokudb/ft-index/ft/dbufio.cc
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="%{optflags} -fno-strict-aliasing"

%cmake	-DINSTALL_LAYOUT=RPM \
	-DMYSQL_DATADIR=/srv/mysql \
	-DMYSQL_UNIX_ADDR=/run/mysqld/mysql.sock \
	-DWITH_EXTRA_CHARSETS=complex \
	-DWITH_LIBEVENT=system

%build
# Used by logformat during build
export LD_LIBRARY_PATH=`pwd`/build/storage/tokudb/ft-index/portability:$LD_LIBRARY_PATH
%make -C build || make -C build

%install
%makeinstall_std -C build

# systemd integration
mkdir -p %{buildroot}/lib/systemd/system
install -c -m 644 %{SOURCE100} %{buildroot}%{_systemunitdir}
install -c -m 755 %{SOURCE101} %{buildroot}%{_bindir}
install -c -m 755 %{SOURCE102} %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_sysconfdir}/init.d

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

%files
# meta package
