#
# Conditional build:
%bcond_without	apidocs		# don't build API documentation
%bcond_without	static_libs	# don't build static libraries

Summary:	Wayland - protocol for a compositor to talk to its clients
Summary(pl.UTF-8):	Wayland - protokół między serwerem składającym a klientami
Name:		wayland
Version:	1.10.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	e7751c38807c231afaba9d6b68f2a2b7
Patch1:		%{name}-man.patch
URL:		https://wayland.freedesktop.org/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	expat-devel >= 1.95
BuildRequires:	libffi-devel >= 3
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
%if %{with apidocs}
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen >= 1.6.0
BuildRequires:	graphviz >= 2.26.0
BuildRequires:	libxslt-progs
BuildRequires:	xmlto
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Wayland is a project to define a protocol for a compositor to talk to
its clients as well as a library implementation of the protocol. The
compositor can be a standalone display server running on Linux kernel
modesetting and evdev input devices, an X application, or a Wayland
client itself. The clients can be traditional applications, X servers
(rootless or fullscreen) or other display servers.

%description -l pl.UTF-8
Wayland to projekt definiujący protokół między serwerem składającym a
klientami, a także biblioteki implementujące ten protokół. Serwer
składający może być samodzielnym serwerem wyświetlającym działającym
na linuksowym kernel modesetting oraz urządzeniach wejściowych evdev,
aplikacją X lub klientem Wayland. Klientami mogą być tradycyjne
aplikacje, serwery X (rootless lub pełnoekranowe) lub inne serwery
wyświetlające.

%package devel
Summary:	Header files for Wayland libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Wayland
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libffi-devel

%description devel
Header files for Wayland libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Wayland.

%package static
Summary:	Static Wayland libraries
Summary(pl.UTF-8):	Statyczne biblioteki Wayland
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Wayland libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Wayland.

%package apidocs
Summary:	Wayland API and protocol documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki oraz protokołu Wayland
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
Wayland API and protocol documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki oraz protokołu Wayland.

%prep
%setup -q
%patch1 -p1

# force regeneration (.so link is broken, double man3/)
%{__rm} doc/man/*.3

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-documentation} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# referenced by some installed wl_*.3 man pages
cp -p doc/doxygen/man/man3/wayland-util.h.3 $RPM_BUILD_ROOT%{_mandir}/man3

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libwayland-*.la
%if %{with apidocs}
# packaged as %doc in -devel
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/wayland
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README TODO
%attr(755,root,root) %{_libdir}/libwayland-client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-client.so.0
%attr(755,root,root) %{_libdir}/libwayland-cursor.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-cursor.so.0
%attr(755,root,root) %{_libdir}/libwayland-server.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-server.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wayland-scanner
%attr(755,root,root) %{_libdir}/libwayland-client.so
%attr(755,root,root) %{_libdir}/libwayland-cursor.so
%attr(755,root,root) %{_libdir}/libwayland-server.so
%{_includedir}/wayland-*.h
%dir %{_datadir}/wayland
%{_datadir}/wayland/wayland.dtd
%{_datadir}/wayland/wayland.xml
%{_datadir}/wayland/wayland-scanner.mk
%{_pkgconfigdir}/wayland-client.pc
%{_pkgconfigdir}/wayland-cursor.pc
%{_pkgconfigdir}/wayland-scanner.pc
%{_pkgconfigdir}/wayland-server.pc
%{_aclocaldir}/wayland-scanner.m4
%if %{with apidocs}
%{_mandir}/man3/wayland-util.h.3*
%{_mandir}/man3/wl_*.3*
%endif

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libwayland-client.a
%{_libdir}/libwayland-cursor.a
%{_libdir}/libwayland-server.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/publican/Wayland/en-US/html/*
%endif
