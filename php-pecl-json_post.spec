%define		php_name	php%{?php_suffix}
%define		modname		json_post
%define		status		stable
Summary:	%{modname} - PHP content type handler for JSON data
Name:		%{php_name}-pecl-%{modname}
Version:	1.0.0
Release:	1
License:	BSD, revised
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	8edd2223bf729c40ad713416ef681361
URL:		http://pecl.php.net/package/json_post/
BuildRequires:	%{php_name}-devel >= 3:5.3.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides a PHP content type handler for
"application/json" and "text/json" to PHP's form data parser. If the
`Content-Type` of an incoming request is `text/json`, the JSON
contents of the request body will by parsed into `$_POST`.

This extension does not provide any constants, functions or classes.

In PECL status of this extension is: %{status}.

%package devel
Summary:	Header files for json_post PECL extension
Group:		Development/Libraries
# does not require base
Requires:	php-devel >= 4:5.2.0

%description devel
Header files for json_post PECL extension.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%{__libtoolize}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

install -D php_json_post.h $RPM_BUILD_ROOT%{_includedir}/php/ext/json_post/php_json_post.h

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so

%files devel
%defattr(644,root,root,755)
%dir %{php_includedir}/ext/json_post
%{php_includedir}/ext/json_post/php_json_post.h
