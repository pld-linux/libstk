# TODO: global fonts installation
Summary:	LibSTK - graphical widget set written in C++
Summary(pl):	LibSTK - zbiór graficznych widgetów napisany w C++
Name:		libstk
Version:	0.2.0
%define	snap	20040208
Release:	0.%{snap}.1
License:	Libstk Library License (relaxed LGPL)
Group:		Libraries
# cvs -d :pserver:anonymous:anonymous@libstk.org:/home/dvhart/cvs/pub co libstk
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	48c7788c2422beba5b8db0c22ad854f1
URL:		http://www.libstk.org/
BuildRequires:	DirectFB-devel
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1.7
BuildRequires:	boost-devel >= 1.30.0
BuildRequires:	freetype-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
#BuildRequires:	xine-lib-devel
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

find . -type d -name CVS | xargs rm -rf

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-directfb \
	--enable-fbdev \
	--enable-sdl
#	--enable-xine - doesn't build (xine headers cause C++ errors)

%{__make} \
	CXXFLAGS="%{rpmcflags} -Wall -W -Wno-switch -pedantic"

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

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
