%define		mod_name	xslt
%define 	apxs		/usr/sbin/apxs
Summary:	Module to serve XML based content
Summary(pl):	Modu³ do udostêpniania dokumentów XML
Name:		apache-mod_%{mod_name}2
Version:	1.3.5
Release:	1
%define snapdate 2004080100
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.mod-xslt2.com/software/archive/%{snapdate}/modxslt-%{snapdate}.tar.gz
# Source0-md5:	5d7f607679a1ffb5dad48a93e655e8ff
Source1:	%{name}.conf
Patch0:		%{name}-makefile.patch
URL:		http://www.mod-xslt2.com/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	libxslt-devel
BuildRequires:	pcre-devel
Requires(post):	/sbin/ldconfig
Requires(post,preun):	%{apxs}
Conflicts:	apache-mod_xslt
Obsoletes:	apache-mod_xslt
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	/etc/httpd

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

%description -l pl
mod_xslt jest prostym modu³em Apache do udostêpniania dokumentów XML.
Dane s± zapisane w plikach XML na serwerze. U¿ytkownik ¿±da pliku XML
i t³maczenia poprzez URL w stylu http://localhost/sourcefile.html.
Modu³ zamienia ten URL na pliki ¼ród³owe XML i XSL. W tym przyk³adzie
plikiem XML bêdzie sourcefile.xml. Modu³ otworzy plik sourcefile.xml i
okre¶li DOCTYPE, na podstawie którego otworzy odpowiedni plik XSL.
Je¿eli DOCTYPE jest "tutorial", plikiem XSL bêdzie tutorial_html.xsl.
Nastêpnie modu³ dokona przetwarzania pliku XML za pomoc± arkusza XSLT
i zwróci przegl±darce powsta³y w ten sposób text/html. Ca³y proces
odbywa siê w sposób niewidoczny dla u¿ytkownika.

%package devel
Summary:	Development headers for mod_xslt2
Summary(pl):	Pliki nag³ówkowe mod_xslt2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
development headers for mod_xslt2.

%package static
Summary:	Static mod_xslt2 library
Summary(pl):	Statyczna biblioteka mod_xslt2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mod_xslt2 library.

%description static -l pl
Statyczna biblioteka mod_xslt2.

%prep
%setup -q -n mod%{mod_name}-%{snapdate}
%patch0 -p1

%build
%configure
%{__make} \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/70_mod_xslt2.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd.conf/*
%attr(755,root,root) %{_pkglibdir}/*
%attr(755,root,root) %{_libdir}/libmodxslt0.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*.la
%{_includedir}/modxslt0

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
