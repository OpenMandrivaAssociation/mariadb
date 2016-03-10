%define beta %{nil}
%define scmrev %{nil}
%define libmajor 18
%define muser mysql
%bcond_without pcre
%define _disable_lto 1

Summary: The MariaDB database, a drop-in replacement for MySQL
Name: mariadb
Version: 10.1.12
Release: 2
URL: http://mariadb.org/
License: GPL
Group: System/Servers
Source0: http://mirrors.n-ix.net/mariadb/mariadb-%{version}/source/mariadb-%{version}.tar.gz
Source1: mysql.tmpfiles.d.in
Source2: mysql.service.in
Source3: mysql-prepare-db-dir.sh
Source4: mysql-wait-ready.sh
Source5: mysql-check-socket.sh
Source6: mysql-scripts-common.sh
Source7: mysql-check-upgrade.sh
Source8: mysql-wait-stop.sh
Source9: mysql@.service.in
Source1000: %{name}.rpmlintrc
# Don't strip -Wformat from --cflags -- -Werror=format-string without -Wformat
# means trouble
Patch0:	mariadb-10.0.8-fix-mysql_config.patch
Patch1: mariadb-10.0.12-clang.patch
Patch2: mariadb-10.1.5-compatibility-with-llvm-ar.patch
Patch3: mariadb-10.1.1-dont-check-null-on-parameters-declared-nonnull.patch
%ifarch %ix86 x86_64
Patch4: mariadb-10.1.5-force-bfd-for-mysqlclient.patch
%endif
# This breaks binary compatibility with some other distributions, but fixes the loading
# of the Qt mysql plugin. Better fix wanted.
Patch5:	mariadb-10.1.10-no-symbol-versioning.patch
%ifnarch %ix86 x86_64
#Patch7: mariadb-10.1.5-fix-version-script-for-gold.patch
%endif
Patch6:	mariadb-10.1.6-fix_atomic_check.patch
Patch7: mariadb-10.1.11-clang.patch
Patch8: mariadb-scripts.patch
Requires: %{name}-server = %{EVRD}
Requires: %{name}-client = %{EVRD}
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	python
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libsystemd-daemon)
BuildRequires:	systemtap
BuildRequires:	libaio-devel
BuildRequires:	stdc++-devel
BuildRequires:	readline-devel
BuildRequires:	xfsprogs-devel
BuildRequires:	jemalloc-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libzmq)
BuildRequires:	pkgconfig(msgpack)
BuildRequires:	lzo-devel
BuildRequires:	wrap-devel
%if %{with pcre}
BuildRequires:	pkgconfig(libpcre)
%endif
# For plugin/auth_pam.so
BuildRequires:	pam-devel
# For plugin/ha_oqgraph.so
BuildRequires:	boost-devel
Obsoletes: mysql < 5.7
Provides: mysql = 5.7

%description
The MariaDB database, a drop-in replacement for MySQL.

%libpackage mysqlclient %{libmajor}
%{_libdir}/libmysqlclient_r.so.%{libmajor}*

%libpackage mysqld %{libmajor}

%define devpackage %mklibname -d mysqlclient

%package -n %{devpackage}
Summary: Development files for the MariaDB database
Provides: %{name}-devel = %{EVRD}
Provides: %{mklibname -d mysqlclient_r} = %{EVRD}
Provides: %{mklibname -d mysqld} = %{EVRD}
Requires: %{mklibname mysqlclient 18} = %{EVRD}
Requires: %{mklibname mysqld 18} = %{EVRD}
Requires: %{name}-common = %{EVRD}
Obsoletes: %{mklibname -d mysql} < %{EVRD}
Provides: %{mklibname -d mysql} = %{EVRD}
%rename mysql-devel
Group: Development/Other

%description -n %{devpackage}
Development files for the MariaDB database.

%files -n %{devpackage}
%{_includedir}/mysql
%{_libdir}/*.so
%{_datadir}/aclocal/mysql.m4
%{_datadir}/pkgconfig/mariadb.pc

%define staticpackage %mklibname -d -s mysqlclient

%package -n %{staticpackage}
Summary: Static libraries for the MariaDB database
Requires: %{devpackage} = %{EVRD}
Provides: %{name}-static-devel = %{EVRD}
Group: Development/Other
Obsoletes: mysql-static-devel < 5.7
Provides: mysql-static-devel = 5.7

%description -n %{staticpackage}
Static libraries for the MariaDB database.

%files -n %{staticpackage}
%{_libdir}/libmysqlclient.a
%{_libdir}/libmysqlclient_r.a
%{_libdir}/libmysqlservices.a

%define staticembpackage %mklibname -d -s mysqld

%package -n %{staticembpackage}
Summary: Static libraries for the Embedded MariaDB database
Provides: %{name}-embedded-static-devel = %{EVRD}
Group: Development/Other
Requires: %{staticpackage} = %{EVRD}

%description -n %{staticembpackage}
Static libraries for the Embedded MariaDB database

%files -n %{staticembpackage}
%{_libdir}/libmysqld.a

%package plugin
Summary: MariaDB plugins
Group: Databases
Obsoletes: mysql-plugin < 5.7
Provides: mysql-plugin = 5.7
Conflicts: mysql-server <= 5.5.30-3

%description plugin
Plugins for the MariaDB database.

%files plugin
%{_libdir}/mysql/plugin/adt_null.so
%{_libdir}/mysql/plugin/auth_0x0100.so
%{_libdir}/mysql/plugin/auth_pam.so
%{_libdir}/mysql/plugin/auth_socket.so
%{_libdir}/mysql/plugin/auth_test_plugin.so
%{_libdir}/mysql/plugin/daemon_example.ini
%{_libdir}/mysql/plugin/dialog.so
%{_libdir}/mysql/plugin/dialog_examples.so
%{_libdir}/mysql/plugin/ha_archive.so
%{_libdir}/mysql/plugin/ha_blackhole.so
%{_libdir}/mysql/plugin/ha_connect.so
%{_libdir}/mysql/plugin/ha_example.so
%{_libdir}/mysql/plugin/ha_federated.so
%{_libdir}/mysql/plugin/ha_federatedx.so
%{_libdir}/mysql/plugin/ha_sphinx.so
%{_libdir}/mysql/plugin/ha_spider.so
%{_libdir}/mysql/plugin/ha_test_sql_discovery.so
%{_libdir}/mysql/plugin/ha_innodb.so
%{_libdir}/mysql/plugin/ha_mroonga.so
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
%{_libdir}/mysql/plugin/semisync_master.so
%{_libdir}/mysql/plugin/semisync_slave.so
%{_libdir}/mysql/plugin/server_audit.so
%{_libdir}/mysql/plugin/sql_errlog.so
%{_mandir}/man1/mysql_plugin.1*
%{_libdir}/mysql/plugin/debug_key_management.so
%{_libdir}/mysql/plugin/example_key_management.so
%{_libdir}/mysql/plugin/file_key_management.so
%{_libdir}/mysql/plugin/simple_password_check.so
%{_libdir}/mysql/plugin/wsrep_info.so

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
%config(noreplace) %{_sysconfdir}/my.cnf.d/tokudb.cnf
%{_bindir}/tokuftdump
%{_bindir}/tokuft_logprint
%endif

%package test
Summary: MariaDB test suite
Group: System/Servers
Obsoletes: mysql-test < 5.7
Provides: mysql-test = 5.7

%description test
MariaDB test suite.

%files test
%{_bindir}/mysqltest
%{_bindir}/mysqltest_embedded
%{_bindir}/mysql_client_test
%{_bindir}/mysql_client_test_embedded
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
Obsoletes: mysql-server < 5.7
Provides: mysql-server = 5.7
Requires(post,preun): rpm-helper

%description server
The MariaDB server. For a full MariaDB database server, install
package '%{name}'.

%pre server
%_pre_useradd %{muser} /srv/mysql /sbin/nologin

%files server
%dir %{_datadir}/mysql
%{_datadir}/mysql/errmsg-utf8.txt
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/install_spider.sql
%{_datadir}/mysql/mysql_performance_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/wsrep_notify
%{_datadir}/mysql/*.cnf
%{_datadir}/mysql/maria_add_gis_sp.sql
%{_datadir}/mysql/maria_add_gis_sp_bootstrap.sql
%{_datadir}/mysql/mroonga
%{_presetdir}/86-mariadb.preset
%{_tmpfilesdir}/%{name}.conf
%{_mandir}/man8/*
%dir %{_libdir}/mysql
%dir %{_libdir}/mysql/plugin
%{_sysconfdir}/logrotate.d/mysql
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
%{_bindir}/wsrep_*
%{_sbindir}/mysqld
%{_bindir}/mariadb-service-convert
%{_sbindir}/mysql-prepare-db-dir
%{_sbindir}/mysql-wait-ready
%{_sbindir}/mysql-wait-stop
%{_sbindir}/mysql-check-socket
%{_sbindir}/mysql-check-upgrade
%{_sbindir}/mysql-scripts-common
%{_unitdir}/*.service
%dir %{_unitdir}/mariadb@bootstrap.service.d
%{_unitdir}/mariadb@bootstrap.service.d/*.conf
%dir %{_datadir}/mysql/systemd
%{_datadir}/mysql/systemd/*.service
%{_datadir}/mysql/systemd/*.conf
%doc %{_docdir}/%{name}-%{version}
%attr(711,%{muser},%{muser}) /srv/mysql
%attr(711,%{muser},%{muser}) %{_localstatedir}/log/mysqld
%{_mandir}/man1/aria_chk.1*
%{_mandir}/man1/aria_dump_log.1*
%{_mandir}/man1/aria_ftdump.1*
%{_mandir}/man1/aria_pack.1*
%{_mandir}/man1/aria_read_log.1*
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_config.1*
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/mysql_fix_extensions.1*
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
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolve_stack_dump.1*
%{_mandir}/man1/resolveip.1*

%package msql2mysql
Summary: Tool to convert code written for mSQL to MySQL/MariaDB
Group: Development/Other

%description msql2mysql
Tool to convert code written for mSQL to MySQL/MariaDB.

%files msql2mysql
%{_bindir}/msql2mysql
%{_mandir}/man1/msql2mysql.1*

%package common
Summary: Common files needed by both the MariaDB server and client
Group: System/Servers
BuildArch: noarch
Obsoletes: mysql-common < 5.7
Provides: mysql-common = 5.7
Requires: %{name}-common-binaries = %{EVRD}

%description common
Common files needed by both the MariaDB server and client.

%files common
%doc README COPYING
%config(noreplace) %{_sysconfdir}/my.cnf
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
%{_datadir}/mysql/policy
# We put this into -common for now because it is needed for both
# -server (used by mysqld_safe) and by -devel (configure scripts calling
# it, e.g. php)
%{_bindir}/mysql_config

%package common-binaries
Summary: Common binary files needed by both the MariaDB server and client
Group: System/Servers
Obsoletes: mysql-common < 5.7
Provides: mysql-common = 5.7
Requires: %{name}-common = %{EVRD}

%description common-binaries
Common files needed by both the MariaDB server and client.

%files common-binaries
%{_bindir}/my_print_defaults
%{_mandir}/man1/my_print_defaults.1*

%package client
Summary: MariaDB command line client
Group: Databases
Obsoletes: mysql-client < 5.7
Provides: mysql-client = 5.7
Conflicts: mysql-server <= 5.5.30-3

%description client
MariaDB command line client.

%files client
%{_bindir}/mysql
%{_bindir}/mysql_embedded
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

%prep
%setup -q
%apply_patches

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} scripts

# Workarounds for bugs
sed -i "s@data/test@\${INSTALL_MYSQLTESTDIR}@g" sql/CMakeLists.txt
#sed -i "s/srv_buf_size/srv_sort_buf_size/" storage/innobase/row/row0log.cc
if echo %{__cc} |grep -q clang; then
sed -e 's, -fuse-linker-plugin,,' -i storage/tokudb/PerconaFT/cmake_modules/TokuSetupCompiler.cmake storage/tokudb/CMakeLists.txt
fi
# -flto doesn't work with the way tokudb builds static libraries
sed -e 's, -flto,,' -i storage/tokudb/PerconaFT/cmake_modules/TokuSetupCompiler.cmake storage/tokudb/CMakeLists.txt

# The version of xz bundled here comes with a version of libtool that doesn't support lto
cd storage/tokudb/PerconaFT/third_party/xz-4.999.9beta
libtoolize --force
aclocal
automake -a
autoconf
cd -

%build
%ifnarch aarch64 %{ix86}
export CC="%{__cc} -Wno-unknown-warning-option -Wno-extern-c-compat -Qunused-arguments"
export CXX="%{__cxx} -Wno-unknown-warning-option -Wno-extern-c-compat -Qunused-arguments"
export CFLAGS="%{optflags} -fno-strict-aliasing -Wno-error=pointer-bool-conversion -Wno-error=missing-field-initializers"
export CXXFLAGS="%{optflags} -fno-strict-aliasing -Wno-error=pointer-bool-conversion -Wno-error=missing-field-initializers -fcxx-exceptions"
%else
# clang 3.7 on i586 fails to build libmysqlclient lib correctly
# ld.gold gives assert in operator() symtab.cc:1656
# ld.bfd gives div error or symver error
export CC=gcc
export CXX=g++
%ifarch x86_64
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="%{optflags} -fno-strict-aliasing"
%endif
%endif

# Get rid of gcc specific flags when using clang
if echo $CC |grep -q gcc; then
export CFLAGS="$CFLAGS -Wno-error=maybe-uninitialized"
export CXXFLAGS="$CXXFLAGS -Wno-error=maybe-uninitialized"
else
sed -i -e 's,-Wstrict-null-sentinel,,;s,-Wtrampolines,,;s,-Wlogical-op,,' storage/tokudb/PerconaFT/cmake_modules/TokuSetupCompiler.cmake
fi

# aliasing rule violations at least in storage/tokudb/PerconaFT/ft/dbufio.cc
# -Wl,--hash-style=both is a workaround for a build failure caused by com_err incorrectly
# thinking it doesn't know about the my_uni_ctype symbol when built with ld 2.24.51.0.3
# and -Wl,--hash-style=gnu
%ifarch %{ix86}
#export LDFLAGS="%{ldflags} -Wl,--hash-style=both"
%else
#export LDFLAGS="%{ldflags} -Wl,--hash-style=both -flto"
#export LDFLAGS="%{ldflags} -Wl,--hash-style=both"
%endif
export LDFLAGS="$LDFLAGS -fuse-ld=bfd"

# (tpg) install services into %_unitdir
sed -i -e "s,/usr/lib/systemd/system,%{_unitdir},g" cmake/install_layout.cmake

%cmake	-DINSTALL_LAYOUT=RPM \
	-DFEATURE_SET="community" \
	-DWITH_SSL=system \
	-DWITH_ZLIB=system \
%if %{with pcre}
	-DWITH_PCRE=system \
%endif
	-DINSTALL_PLUGINDIR="%{_libdir}/mysql/plugin" \
	-DINSTALL_LIBDIR="%{_libdir}" \
	-DMYSQL_DATADIR=/srv/mysql \
	-DMYSQL_UNIX_ADDR=/run/mysqld/mysql.sock \
	-DWITH_EXTRA_CHARSETS=complex \
	-DWITH_EMBEDDED_SERVER:BOOL=ON \
	-DWITH_READLINE:BOOL=ON \
	-DWITH_LIBEVENT=system \
	-DINSTALL_SYSTEMD_UNITDIR_RPM="%{_unitdir}" \
	-DCOMPILATION_COMMENT="%{_vendor} MariaDB Server"

# Used by logformat during build
export LD_LIBRARY_PATH=`pwd`/storage/tokudb/PerconaFT/portability:$LD_LIBRARY_PATH
%make -k || make

%install
%makeinstall_std -C build

# systemd integration
rm -rf %{buildroot}%{_sysconfdir}/init.d
rm -f %{buildroot}%{_sbindir}/rcmysql
install -D -p -m 644 build/scripts/mysql.service %{buildroot}%{_unitdir}/%{name}.service
install -D -p -m 644 build/scripts/mysql@.service %{buildroot}%{_unitdir}/%{name}@.service
install -D -p -m 0644 build/scripts/mysql.tmpfiles.d %{buildroot}%{_tmpfilesdir}/%{name}.conf

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-mariadb.preset << EOF
enable mariadb.service
EOF

# helper scripts for service starting
install -D -p -m 755 build/scripts/mysql-prepare-db-dir %{buildroot}%{_sbindir}/mysql-prepare-db-dir
install -p -m 755 build/scripts/mysql-wait-ready %{buildroot}%{_sbindir}/mysql-wait-ready
install -p -m 755 build/scripts/mysql-wait-stop %{buildroot}%{_sbindir}/mysql-wait-stop
install -p -m 755 build/scripts/mysql-check-socket %{buildroot}%{_sbindir}/mysql-check-socket
install -p -m 755 build/scripts/mysql-check-upgrade %{buildroot}%{_sbindir}/mysql-check-upgrade
install -p -m 644 build/scripts/mysql-scripts-common %{buildroot}%{_sbindir}/mysql-scripts-common

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
