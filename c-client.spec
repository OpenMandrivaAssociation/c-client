%define fversion 2007d
%define soname c-client

%define major 0
%define libname %mklibname %{soname} %{major}
%define develname %mklibname -d %{soname}

Summary:	UW-IMAP C-CLIENT library
Name:		c-client
Version:	2007d
Release:	%mkrel 2
License:	Apache License
Group:		System/Servers
URL:		http://www.washington.edu/imap/
Source:		ftp://ftp.cac.washington.edu/mail/imap-%{fversion}.tar.Z
Source7:	flock.c
Source8:	Makefile.imap
Patch0: 	imap-2002e-ssl.patch
Patch1: 	imap-2007a-linux.diff
Patch3:		imap-2001a-disable-mbox.patch
Patch4:		imap-2001a-redhat.patch
Patch5: 	imap-2006c1-flock.diff
Patch9:		imap-2006c1-glibc-2.2.2.diff
Patch11:	imap-2006c1-krbpath.diff
Patch12:	imap-2001a-overflow.patch
Patch17:	imap-mail-spool-perms.diff
Patch21:	imap-2004a-shared.patch
Patch22:	imap-2002e-authmd5.patch
# (oe) the annotate patch is implemented upstream and needed by kolab2
Patch23:	imap-2006c1-annotate.diff
# (oe) http://www.gadgetwiz.com/software/hash_reset.html
Patch24:	imap-2004g-hash_reset.diff
Patch25:	imap-yes.diff
BuildRequires:	openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The c-client library is a common API for accessing mailboxes developed at
the University of Washington. It is used mainly by php in Mandriva Linux.

%package -n	%{libname}
Summary:	C-client mail access routines for IMAP and POP protocols
Group:		System/Libraries
Provides:	c-client = %{version}-%{release}

%description -n	%{libname}
The c-client library is a common API for accessing mailboxes developed at
the University of Washington. It is used mainly by php in Mandriva Linux.

This package contains the shared c-client library.

%package -n	%{develname}
Summary:	Development files for the c-client library
Group:		Development/C
Requires:	%{libname} = %{version}
Obsoletes:	libc-client-php-devel
Obsoletes:	%{mklibname c-client-php -d 0}
Obsoletes:	imap-devel
Provides:	c-client-devel = %{version}-%{release}

%description -n	%{develname}
The c-client library is a common API for accessing mailboxes developed at
the University of Washington. It is used mainly by php in Mandriva Linux.

This package contains development files for the c-client library.

%prep

%setup -q -n imap-%{version}

%patch0 -p0 -b .ssl
%patch1 -p0 -b .linux
%patch3 -p1 -b .mbox
%patch4 -p1 -b .redhat
%patch5 -p0 -b .flock
install -m 0644 %{SOURCE7} src/osdep/unix/flock.c
%patch9 -p1 -b .glibc

%patch12 -p1 -b .overflow
%patch17 -p0 -b .lock-warning
%patch21 -p1 -b .shared
%patch22 -p1 -b .authmd5
%patch23 -p1 -b .annotate
%patch24 -p1 -b .hash_reset
%patch25 -p0 -b .yes

%build
%serverbuild

touch ip6
EXTRACFLAGS="$EXTRACFLAGS -DDISABLE_POP_PROXY=1 -DIGNORE_LOCK_EACCES_ERRORS=1 -I%{_includedir}/openssl"
EXTRALDFLAGS="$EXTRALDFLAGS -L%{_libdir}"
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D_REENTRANT -DDIC -fPIC -fno-omit-frame-pointer" slx \
	EXTRACFLAGS="$EXTRACFLAGS" \
	EXTRALDFLAGS="$EXTRALDFLAGS" \
	SSLDIR=%{_libdir}/ssl \
	SSLINCLUDE=%{_includedir}/openssl \
	SSLLIB=%{_libdir} \
	LOCKPGM=%{_sbindir}/mlock \
	SSLTYPE=unix \
	SHLIBBASE=%{soname} \
	SHLIBNAME=lib%{soname}.so.%{major} \
	BASECFLAGS="$RPM_OPT_FLAGS -D_REENTRANT -DDIC -fPIC -fno-omit-frame-pointer" \
	IP=6

mv -f c-client/c-client.a %{soname}.a
mv -f c-client/lib%{soname}.so.%{major} .

%install
rm -rf %{buildroot}

# make some directories
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}/imap

# install headers
install -m0644 c-client/*.h %{buildroot}%{_includedir}/imap/
install -m0644 src/osdep/tops-20/shortsym.h %{buildroot}%{_includedir}/imap/
install -m0644 src/osdep/tops-20/linkage.c %{buildroot}%{_includedir}/imap/

install -m0755 lib%{soname}.so.%{major} %{buildroot}%{_libdir}/
ln -snf lib%{soname}.so.%{major} %{buildroot}%{_libdir}/lib%{soname}.so
install -m0644 %{soname}.a %{buildroot}%{_libdir}/lib%{soname}.a

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib%{soname}.so.%{major}

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/imap
%{_libdir}/lib%{soname}.a
%{_libdir}/lib%{soname}.so
