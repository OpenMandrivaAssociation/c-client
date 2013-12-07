%define _disable_ld_no_undefined 1

%define fversion 2007f
%define soname c-client

%define major	0
%define libname %mklibname %{soname} %{major}
%define devname %mklibname -d %{soname}

Summary:	UW-IMAP C-CLIENT library
Name:		c-client
Version:	2007f
Release:	6
License:	Apache License
Group:		System/Servers
Url:		http://www.washington.edu/imap/
Source0:	ftp://ftp.cac.washington.edu/mail/imap-%{fversion}.tar.gz
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
BuildRequires:	pkgconfig(openssl)

%description
The c-client library is a common API for accessing mailboxes developed at
the University of Washington. It is used mainly by php in Mandriva Linux.

%package -n	%{libname}
Summary:	Mail access routines for IMAP and POP protocols
Group:		System/Libraries
Provides:	c-client = %{version}-%{release}

%description -n	%{libname}
The c-client library is a common API for accessing mailboxes developed at
the University of Washington. It is used mainly by php in Mandriva Linux.

This package contains the shared c-client library.

%package -n	%{devname}
Summary:	Development files for the c-client library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	c-client-devel = %{version}-%{release}

%description -n	%{devname}
The c-client library is a common API for accessing mailboxes developed at
the University of Washington. It is used mainly by php in Mandriva Linux.

This package contains development files for the c-client library.

%prep
%setup -qn imap-%{version}
%patch0 -p0 -b .ssl
%patch1 -p0 -b .linux
%patch3 -p1 -b .mbox
%patch4 -p0 -b .redhat
%patch5 -p0 -b .flock
install -m 0644 %{SOURCE7} src/osdep/unix/flock.c
%patch9 -p1 -b .glibc

%patch12 -p0 -b .overflow
%patch17 -p0 -b .lock-warning
%patch21 -p0 -b .shared
%patch22 -p1 -b .authmd5
%patch23 -p1 -b .annotate
%patch24 -p1 -b .hash_reset
%patch25 -p0 -b .yes

%build
%serverbuild
export CFLAGS="%{optflags} -fPIC"
touch ip6
export EXTRACFLAGS="$EXTRACFLAGS $CFLAGS -DDISABLE_POP_PROXY=1 -DIGNORE_LOCK_EACCES_ERRORS=1 -I%{_includedir}/openssl -D_GNU_SOURCE"
export EXTRALDFLAGS="$EXTRALDFLAGS -L%{_libdir} %{ldflags}"

make RPM_OPT_FLAGS="$CFLAGS -D_REENTRANT -DDIC -fPIC -fno-omit-frame-pointer -D_GNU_SOURCE" slx \
	EXTRACFLAGS="$EXTRACFLAGS" \
	EXTRALDFLAGS="$EXTRALDFLAGS" \
	SSLDIR=%{_libdir}/ssl \
	SSLINCLUDE=%{_includedir}/openssl \
	SSLLIB=%{_libdir} \
	LOCKPGM=%{_sbindir}/mlock \
	SSLTYPE=unix \
	SHLIBBASE=%{soname} \
	SHLIBNAME=lib%{soname}.so.%{major} \
	BASECFLAGS="$CFLAGS -D_REENTRANT -DDIC -fPIC -fno-omit-frame-pointer -D_GNU_SOURCE" \
	IP=6

mv -f c-client/c-client.a %{soname}.a
mv -f c-client/lib%{soname}.so.%{major} .

%install
# make some directories
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}/imap

# install headers
install -m0644 c-client/*.h %{buildroot}%{_includedir}/imap/
install -m0644 src/osdep/tops-20/shortsym.h %{buildroot}%{_includedir}/imap/
install -m0644 src/osdep/tops-20/linkage.c %{buildroot}%{_includedir}/imap/

install -m0755 lib%{soname}.so.%{major} %{buildroot}%{_libdir}/
ln -snf lib%{soname}.so.%{major} %{buildroot}%{_libdir}/lib%{soname}.so
#install -m0644 %{soname}.a %{buildroot}%{_libdir}/lib%{soname}.a

%files -n %{libname}
%{_libdir}/lib%{soname}.so.%{major}

%files -n %{devname}
%{_includedir}/imap
%{_libdir}/lib%{soname}.so

