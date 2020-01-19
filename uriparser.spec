Name:           uriparser
Version:        0.7.5
Release:        7%{?dist}
Summary:        URI parsing library - RFC 3986

Group:          System Environment/Libraries
License:        BSD
URL:            http://%{name}.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         uriparser-0.7.5-doc_Makefile_in.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  doxygen, graphviz, cpptest-devel
Requires:       cpptest

%description
Uriparser is a strictly RFC 3986 compliant URI parsing library written
in C. uriparser is cross-platform, fast, supports Unicode and is
licensed under the New BSD license.

%package	devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .doc_Makefile_in
sed -i 's/\r//' THANKS
sed -i 's/\r//' COPYING
iconv -f iso-8859-1 -t utf-8 -o THANKS{.utf8,}
mv THANKS{.utf8,}

%build
%configure --disable-static
cd doc;

# Remove qhelpgenerator dependency, by commenting these lines in
# Doxygen.in
## .qch output
## QCH_FILE = "../uriparser-doc-0.7.5.qch"
## QHG_LOCATION = "qhelpgenerator"
sed -i 's/^# .qch output.*//' Doxyfile.in
sed -i 's/^QCH.*//' Doxyfile.in
sed -i 's/^QHG.*//' Doxyfile.in

%configure; make %{?_smp_mflags}; cd ..
make %{?_smp_mflags}

# doc folder has separate configure file
#cd doc;
# fix for automated autotool calls
#touch aclocal.m4 configure Makefile.in
#%configure; make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
mv $RPM_BUILD_ROOT/%{_datadir}/doc/uriparser/html \
 $RPM_BUILD_ROOT/%{_datadir}/doc/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc THANKS AUTHORS COPYING ChangeLog
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 07 2010 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.5-3
- Fixed FTBFS

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 06 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.5-1
- Upgrade to 0.7.5:
-  Improved docs
-  Test suite
- 0.7.4
-  Cleaned up code and fixed memory leaks
- 0.7.3
-  Builds for Cygwin, minor bug fix
-  Changes in build system.
-  Added: Qt Assistant documentation output
- 0.7.2
-  Improved and cleaned API 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep 06 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-6
- changed document file handling in spec, used better method - %%doc

* Fri Sep 05 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-5
- fixed group, removed redundant args for %%setup
- included ChangeLog, fixed html folder path in %%files
- fixed automated autotool calls

* Sat Aug 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-4
- changed name according to naming guidelines

* Sat Aug 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-3
- fixed buildrequires tag

* Sun Aug 10 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-2
- added documentation

* Sat Aug 9 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-1
- Initial build
