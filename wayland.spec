#
# Conditional build:
%bcond_without	apidocs		# don't build API documentation
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Wayland - protocol for a compositor to talk to its clients
Summary(pl.UTF-8):	Wayland - protokół między serwerem składającym a klientami
Name:		wayland
Version:	1.0.4
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	1cdc3952001d85629e68b10a9e95a13c
Patch0:		%{name}-publican.patch
Patch1:		%{name}-missing.patch
URL:		http://wayland.freedesktop.org/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	libffi-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libffi)
%{?with_apidocs:BuildRequires:	publican >= 3}
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

%description apidocs
Wayland API and protocol documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki oraz protokołu Wayland.

%prep
%setup -q

# this file is required by publican 3.0; publican patch adds it in en-US dir
test ! -f doc/Wayland/en_US/Revision_History.xml

%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libwayland-*.la
# packaged as %doc in -devel
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/wayland

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
%{_pkgconfigdir}/wayland-client.pc
%{_pkgconfigdir}/wayland-cursor.pc
%{_pkgconfigdir}/wayland-server.pc
%{_aclocaldir}/wayland-scanner.m4
%{_aclocaldir}/wayland-scanner.mk
%{_mandir}/man3/wl_display_connect.3*
%{_mandir}/man3/wl_display_connect_to_fd*

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
%doc doc/Wayland/Wayland/en-US/html/*
%endif
