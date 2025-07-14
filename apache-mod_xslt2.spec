# TODO
# - update to current apr, apu
%define		mod_name	xslt
%define		apxs		/usr/sbin/apxs
%define		snap		337e290
Summary:	Module to serve XML based content
Summary(pl.UTF-8):	Moduł do udostępniania dokumentów XML
Name:		apache-mod_%{mod_name}2
Version:	1.4.1
Release:	0.1
License:	GPL
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/ccontavalli/mod-xslt/tarball/v1.4.1#/%{name}-%{version}.tar.gz
# Source0-md5:	71cbec1d497a3264633cc50dccc6c7a3
Source1:	%{name}.conf
Patch0:		%{name}-makefile.patch
URL:		http://www.mod-xslt2.com/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	libxslt-devel
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,postun):	/sbin/ldconfig
Requires:	apache(modules-api) = %apache_modules_api
Conflicts:	apache-mod_xslt
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_xslt is a simple Apache module to serve XML based content. Data is
stored in XML files on the server. The user requests the XML file and
the translation method via a url such as this:
http://localhost/sourcefile.html. The module will parse this URL into
a XML source file and an XSL source file. In the example above, the
XML file will be sourcefile.xml. The module will open sourcefile.xml
and determine its DOCTYPE. Based on the DOCTYPE, the XSL file will be
opened. Should the DOCTYPE be "tutorial", the XSL file opened would be
tutorial_html.xsl. The content-type returned to the browser is
text/html. The translation occurs transparently to the user.

%description -l pl.UTF-8
mod_xslt jest prostym modułem Apache do udostępniania dokumentów XML.
Dane są zapisane w plikach XML na serwerze. Użytkownik żąda pliku XML
i tłumaczenia poprzez URL w stylu http://localhost/sourcefile.html.
Moduł zamienia ten URL na pliki źródłowe XML i XSL. W tym przykładzie
plikiem XML będzie sourcefile.xml. Moduł otworzy plik sourcefile.xml i
określi DOCTYPE, na podstawie którego otworzy odpowiedni plik XSL.
Jeżeli DOCTYPE jest "tutorial", plikiem XSL będzie tutorial_html.xsl.
Następnie moduł dokona przetwarzania pliku XML za pomocą arkusza XSLT
i zwróci przeglądarce powstały w ten sposób text/html. Cały proces
odbywa się w sposób niewidoczny dla użytkownika.

%package devel
Summary:	Development headers for mod_xslt2
Summary(pl.UTF-8):	Pliki nagłówkowe mod_xslt2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
development headers for mod_xslt2.

%package static
Summary:	Static mod_xslt2 library
Summary(pl.UTF-8):	Statyczna biblioteka mod_xslt2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mod_xslt2 library.

%description static -l pl.UTF-8
Statyczna biblioteka mod_xslt2.

%prep
%setup -q -n ccontavalli-mod-xslt-%{snap}
%patch -P0 -p1

%build
%configure \
	--with-sapi=apache2 \
	--with-apr-config=%{_bindir}/apr-1-config \
	--with-apu-config=%{_bindir}/apu-1-config \
	--with-apxs=%{apxs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/70_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%service -q httpd restart

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%attr(755,root,root) %{_libdir}/libmodxslt1.so.*.*.*
%{_mandir}/man1/modxslt-config.1*
%{_mandir}/man1/modxslt-parse.1*
%{_mandir}/man1/modxslt-perror.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*.la
%{_includedir}/modxslt1

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
