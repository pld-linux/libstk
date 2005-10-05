#
# TODO: global fonts installation
#
# Conditional build:
%bcond_without	static_libs 	# build without static libraries
%bcond_without	xine		# build without xine support
#
Summary:	LibSTK - graphical widget set written in C++
Summary(pl):	LibSTK - zbiór graficznych widgetów napisany w C++
Name:		libstk
Version:	0.2.0
%define	snap	20040507
Release:	0.%{snap}.8
License:	Libstk Library License (relaxed LGPL)
Group:		Libraries
# cvs -d :pserver:anonymous:anonymous@libstk.org:/home/dvhart/cvs/pub co libstk
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	fbcab2be93acd3d66b9e7961fd92bec9
Patch0:		%{name}-fixes.patch
Patch1:		%{name}-gcc34.patch
URL:		http://www.libstk.org/
BuildRequires:	DirectFB-devel
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1:1.7
BuildRequires:	boost-bind-devel >= 1.32.0
BuildRequires:	boost-conversion-devel >= 1.32.0
BuildRequires:	boost-devel >= 1.32.0
BuildRequires:	boost-signals-devel >= 1.32.0
BuildRequires:	boost-thread-devel >= 1.32.0
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

%description -l pl
LibSTK to zestaw widgetów graficznych zaprojektowany aby sprostaæ
dzisiejszym potrzebom pojawiaj±cej siê klasy platform z osadzonymi
mediami. LibSTK tworzy abstrakcjê systemów grafiki i zdarzeñ,
pozwalaj±c na u¿ywanie ich na ka¿dej platformie z kompilatorem zgodnym
z C++.

%package devel
Summary:	Header files for LibSTK library
Summary(pl):	Pliki nag³ówkowe biblioteki LibSTK
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
BuildRequires:	DirectFB-devel
Requires:	SDL-devel >= 1.2.0
Requires:	boost-bind-devel >= 1.32.0
Requires:	boost-devel >= 1.32.0
Requires:	boost-signals-devel >= 1.32.0
Requires:	boost-thread-devel >= 1.32.0
Requires:	freetype-devel >= 2.0
Requires:	libjpeg-devel
Requires:	libpng-devel
%{?with_xine:Requires:	xine-lib-devel}

%description devel
Header files for LibSTK library.

%description devel -l pl
Pliki nag³ówkowe biblioteki LibSTK.

%package static
Summary:	Static LibSTK library
Summary(pl):	Statyczna biblioteka LibSTK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LibSTK library.

%description static -l pl
Statyczna biblioteka LibSTK.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

find . -type d -name CVS | xargs rm -rf

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
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/libstk-*
%{_pkgconfigdir}/*.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
