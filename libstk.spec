#
# TODO: global fonts installation
#
# Workaround for xine-lib.spec - libstk.spec updating:
#       1. make-request -r --without stk xine-lib
#       2. make-request -r libstk
#	3. bump release of xine-lib
#	4. make-request -r xine-lib
#
# Conditional build:
%bcond_without	static_libs 	# static library
%bcond_without	xine		# XINE support
%bcond_without	apidocs		# API/internal docs in HTML format
#
%define		snap	20070719
%define		rel	1
Summary:	LibSTK - graphical widget set written in C++
Summary(pl.UTF-8):	LibSTK - zbiór graficznych widgetów napisany w C++
Name:		libstk
Version:	0.2.0
Release:	0.%{snap}.%{rel}
License:	Libstk Library License (relaxed LGPL)
Group:		Libraries
# https://github.com/dvhart/libstk/tarball/master snapshotted after last commit on %{snap}
#Source0:	http://www.libstk.net/sites/www.libstk.net/files/%{name}-%{snap}.tar.gz
Source0:	%{name}-%{snap}.tar.gz
# Source0-md5:	59ecdb5f78298896a415abe05855b62e
Patch0:		%{name}-fixes.patch
Patch1:		%{name}-am.patch
Patch2:		%{name}-xine.patch
Patch3:		%{name}-xsl.patch
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
%{?with_xine:BuildRequires:	xine-lib-devel >= 2:1.2}
%if %{with apidocs}
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	graphviz
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
%endif
Requires:	fonts-TTF-bitstream-vera
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
Requires:	DirectFB-devel
Requires:	SDL-devel >= 1.2.0
Requires:	boost-devel >= 1.35.0
Requires:	freetype-devel >= 2.0
Requires:	libjpeg-devel
Requires:	libpng-devel
%{?with_xine:Requires:	xine-lib-devel >= 2:1.2}

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
%setup -q -n dvhart-libstk-6186fff
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__rm} doc/images/doc_images_go_here

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

%if %{with apidocs}
cd doc
./process_xml.sh
mv -f output html
mv -f images html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_datadir}/%{name}/fonts
for FONT in Vera*.ttf; do
	%{__rm} "$FONT"
	ln -s %{_datadir}/fonts/TTF/"$FONT" "$FONT"
done
%{__rm} copyright

# just tests, don't package them
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{hello_world,hydra,test_app,test_area,timer_test,xine_test}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO doc/license.txt
%attr(755,root,root) %{_libdir}/libstk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstk.so.0
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%doc doc/{dvhart_carter_architecture.txt,irc_*.txt,uml.jpg,widget_tree.txt} %{?with_apidocs:doc/html}
%attr(755,root,root) %{_libdir}/libstk.so
%{_libdir}/libstk.la
%{_includedir}/libstk-0.2.0
%{_pkgconfigdir}/libstk.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libstk.a
%endif
