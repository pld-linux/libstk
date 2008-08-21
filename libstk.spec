#
# TODO: global fonts installation
#
# Conditional build:
%bcond_without	static_libs 	# build without static libraries
%bcond_without	xine		# build without xine support
#
Summary:	LibSTK - graphical widget set written in C++
Summary(pl.UTF-8):	LibSTK - zbiór graficznych widgetów napisany w C++
Name:		libstk
Version:	0.2.0
%define		snap	20061117
Release:	0.%{snap}.12
License:	Libstk Library License (relaxed LGPL)
Group:		Libraries
#Source0:	http://www.libstk.net/sites/www.libstk.net/files/%{name}-%{snap}.tar.gz
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	350c5e47de8a54d19372bcf6ca926540
Patch0:		%{name}-fixes.patch
URL:		http://www.libstk.net/
BuildRequires:	DirectFB-devel
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1:1.7
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
%{?with_xine:BuildRequires:	xine-lib-devel}
%{?with_xine:Provides:	%{name}(xine) = %{version}-%{release}}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibSTK is graphical widget set designed to meet the needs of today's
emerging class of embedded media platforms, such as set-top boxes, and
vehicular media systems. LibSTK abstracts the graphic and event
systems, allowing it to be used on any platform with a C++-compliant
compiler.

%description -l pl.UTF-8
LibSTK to zestaw widgetów graficznych zaprojektowany aby sprostać
dzisiejszym potrzebom pojawiającej się klasy platform z osadzonymi
mediami. LibSTK tworzy abstrakcję systemów grafiki i zdarzeń,
pozwalając na używanie ich na każdej platformie z kompilatorem zgodnym
z C++.

%package devel
Summary:	Header files for LibSTK library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LibSTK
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
BuildRequires:	DirectFB-devel
Requires:	SDL-devel >= 1.2.0
Requires:	boost-devel >= 1.35.0
Requires:	freetype-devel >= 2.0
Requires:	libjpeg-devel
Requires:	libpng-devel
%{?with_xine:Requires:	xine-lib-devel}

%description devel
Header files for LibSTK library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LibSTK.

%package static
Summary:	Static LibSTK library
Summary(pl.UTF-8):	Statyczna biblioteka LibSTK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LibSTK library.

%description static -l pl.UTF-8
Statyczna biblioteka LibSTK.

%prep
%setup -q -n %{name}-%{snap}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# workaround for xine headers
CPPFLAGS="-DHAVE_BASENAME"
%configure \
	--enable-directfb \
	--enable-fbdev \
	--enable-sdl \
	%{!?with_static_libs:--enable-static=no} \
	%{?with_xine:--enable-xine}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f doc/license.txt .

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO license.txt
%attr(755,root,root) %{_libdir}/libstk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstk.so.0
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_libdir}/libstk.so
%{_libdir}/libstk.la
%{_includedir}/libstk-*
%{_pkgconfigdir}/libstk.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libstk.a
%endif
