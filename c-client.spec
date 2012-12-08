%define _disable_ld_no_undefined 1

%if %mdkversion < 200900
%define ldflags %{nil}
%endif

%define fversion 2007f
%define soname c-client

%define major 0
%define libname %mklibname %{soname} %{major}
%define develname %mklibname -d %{soname}

Summary:	UW-IMAP C-CLIENT library
Name:		c-client
Version:	2007f
Release:	%mkrel 2
License:	Apache License
Group:		System/Servers
URL:		http://www.washington.edu/imap/
Source:		ftp://ftp.cac.washington.edu/mail/imap-%{fversion}.tar.gz
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


%changelog
* Fri Aug 12 2011 Oden Eriksson <oeriksson@mandriva.com> 2007f-1mdv2011.0
+ Revision: 694094
- 2007f

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2007e-6
+ Revision: 663347
- mass rebuild

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 2007e-5mdv2011.0
+ Revision: 603813
- rebuild

* Fri Apr 09 2010 Funda Wang <fwang@mandriva.org> 2007e-4mdv2010.1
+ Revision: 533316
- rebuild

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 2007e-3mdv2010.1
+ Revision: 511554
- rebuilt against openssl-0.9.8m

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 2007e-2mdv2010.0
+ Revision: 413202
- rebuild

* Wed Jan 14 2009 Oden Eriksson <oeriksson@mandriva.com> 2007e-1mdv2009.1
+ Revision: 329246
- 2007e
- rediff patches
- really use CFLAGS and LDFLAGS (but disable --no-undefined)
- use -D_GNU_SOURCE (avoid possible ipv6 problems...)

* Thu Dec 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2007d-3mdv2009.1
+ Revision: 315821
- really utilize LDFLAGS (as the mandriva rpm macros see it)

* Thu Dec 11 2008 Oden Eriksson <oeriksson@mandriva.com> 2007d-2mdv2009.1
+ Revision: 313373
- use "%%define _default_patch_fuzz 2" because i can
- add the linkage.c file, needed by upcoming asterisk

* Wed Nov 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2007d-1mdv2009.1
+ Revision: 300071
- 2007d

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2007b-1mdv2009.0
+ Revision: 238130
- 2007b

* Thu Jul 10 2008 Oden Eriksson <oeriksson@mandriva.com> 2007a-2mdv2009.0
+ Revision: 233346
- fix deps

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 2007a-1mdv2009.0
+ Revision: 233136
- import c-client


* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 2007a-1mdv2009.0
- the rebirth release

+ Revision: 218128
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2007a-1mdv2009.0
+ Revision: 208746
- 2007a1
- rediffed P1

* Tue Feb 19 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2006k-1mdv2008.1
+ Revision: 173159
- 2006k

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tvignaud@mandriva.com> 1:2006j-1mdv2008.1
+ Revision: 127021
- kill re-definition of %%buildroot on Pixel's request

* Mon Aug 06 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2006j-1mdv2008.0
+ Revision: 59326
- fix rpmlint upload blockers
- 2006j
- obey new devel naming specs

* Fri Jun 22 2007 Andreas Hasenack <andreas@mandriva.com> 1:2006i-2mdv2008.0
+ Revision: 43197
- use serverbuild macro

* Thu Jun 21 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2006i-1mdv2008.0
+ Revision: 42301
- 2006i
- drop the version patch (P7) as it is quite useless

* Thu May 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2006h-1mdv2008.0
+ Revision: 26081
- 2006h
- rediffed some patches
- removed obsolete patches
- added one patch to skip the y/n prompt


* Thu Nov 23 2006 Andreas Hasenack <andreas@mandriva.com> 2006c1-2mdv2007.0
+ Revision: 86682
- drop USERID from xinetd (#27278)
- drop svn warning from spec file

* Fri Oct 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2006c1-1mdv2007.1
+ Revision: 73101
- 2006c1
- new license BSD/Apache License
- rediffed patches; P1,P5,P7,P9,P11,P17,P23

* Sun Aug 13 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2004g-2mdv2007.0
+ Revision: 55717
- correct the pam file generation
- fix a possible symbol clash with mysql

* Tue Aug 08 2006 Andreas Hasenack <andreas@mandriva.com> 1:2004g-1mdv2007.0
+ Revision: 54213
- ops, 200700 and not 20070 in mkdversion comparison
- updated to version 2004g (using pristine version: .Z)
- removed CAN-2005-2933 security patch, already fixed
- bunzipped rest of bzipped source files
- build pam file according to version of the distribution
- using mdv instead of mdk in the version patch which marks this
  as a modified version of the software
- import imap-2004e-3mdk

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2004e-3mdk
- rebuilt against openssl-0.9.8a

* Tue Oct 25 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2004e-2mdk
- security update for CAN-2205-2933 (P24)

* Thu Jul 07 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2004e-1mdk
- 2004e
- added rediffed P23 from the openpkg kolab2 packages

* Fri Jun 10 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2004d-2mdk
- Rebuild for libkrb53-devel 1.4.1

* Mon May 30 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1:2004d-1mdk
- 2004d
- rediffed P1

* Thu Feb 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1:2004c1-2mdk
- fix xinetd deps (#13716)

* Sun Feb 13 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1:2004c1-1mdk
- 2004c1 (maintenance release)
- rediffed P7
- drop P30, the vu-702777 fix is included upstream
- added some ssl related build stuff after looking at the new lmd 
  build option

* Sat Feb 12 2005 Stew Benedict <sbenedict@mandrakesoft.com> 1:2004a-2mdk
- security update for CERT VU#702777 (p30)
- rpmlint:
    o drop unused patch, dot in summary
    o requires-release, incoherant version,
- drop compatibility defines for ancient distro releases

* Tue Nov 09 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2004a-1mdk
- 2004a (maintenance release)
- rediffed P7

* Fri Oct 22 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2004-2mdk
- use -D_REENTRANT -DDIC, seems to fix amd64 build (joeghi)
- fix P21 (joeghi)

* Thu Jun 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2004-1mdk
- 2004
- enabled ipv6 support
- fixed P1, P5, P7, P9
- drop pointless P10
- disable pam in the shared c-client lib, pretty pointless for a  
  php-imap client...

* Wed Jun 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2002e-1mdk
- 2002e
- provide shared c-client libs as well

* Mon Dec 29 2003 Stew Benedict <sbenedict@mandrakesoft.com> 2002d-8mdk
- msec/ipop3d conflict with mailbox permissions [Bug 6617] - Patch17
- some file re-arranging to make rpmlint happier

