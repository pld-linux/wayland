#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Wayland - protocol for a compositor to talk to its clients
Summary(pl.UTF-8):	Wayland - protokół między serwerem składającym a klientami
Name:		wayland
Version:	0.85.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	fe3fdfdcc0b20235a113e0e34a665b1c
URL:		http://wayland.freedesktop.org/
BuildRequires:	expat-devel
BuildRequires:	libffi-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libffi)
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

%prep
%setup -q

%build
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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_libdir}/libwayland-client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-client.so.0
%attr(755,root,root) %{_libdir}/libwayland-server.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwayland-server.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wayland-scanner
%attr(755,root,root) %{_libdir}/libwayland-client.so
%attr(755,root,root) %{_libdir}/libwayland-server.so
%{_includedir}/wayland-*.h
%{_pkgconfigdir}/wayland-client.pc
%{_pkgconfigdir}/wayland-server.pc
%{_aclocaldir}/wayland-scanner.m4
%{_aclocaldir}/wayland-scanner.mk

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libwayland-client.a
%{_libdir}/libwayland-server.a
%endif
