Summary:	Dhcp IP status cgi
Name:		dhcpstatus
Version:	0.60
Release:	24
License:	GPLv2
Group:		Monitoring
Url:		http://dhcpstatus.sourceforge.net
Source0:	%{name}_%{version}.tar.bz2
Source1:	%{name}_%{version}.patch
#Source2:	%{name}_%{version}-lib.patch.bz2
BuildArch:	noarch
Requires:	dhcp-server
Requires:	perl-CGI

%description
DHCP-Status is basically two Perl CGI scripts that provide an overall picture
of the information contained in the dhcpd.conf and dhcpd.leases files that
are used by ISC's DHCP server, DHCPD.

%prep
%setup -qn %{name}_%{version}

%build

%install
mkdir -p %{buildroot}%{perl_vendorlib}/%{name}
mkdir -p %{buildroot}%{_docdir}/%{name}_%{version}
mkdir -p %{buildroot}/var/www/cgi-bin
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/
tar xf libraries.tar
# TODO: Fix Apply patch 
bzcat %{SOURCE1} | patch -p0
#bzcat %{SOURCE2} | patch -p0

cp -a %{name}/*.pm %{buildroot}/%perl_vendorlib/%{name}
cp -a {README,INSTALL,LICENSE} %{buildroot}%{_docdir}/%{name}_%{version}
cp -a scripts/*.cgi %{buildroot}/var/www/cgi-bin
cp -a scripts/%{name} %{buildroot}/%{_bindir}
cp -a *.ini %{buildroot}/%{_sysconfdir}/
sed -i -e 's|/etc/dhcpd\.leases|%{_localstatedir}/lib/dhcp/dhcpd.leases|' %{buildroot}/var/www/cgi-bin/%{name}.cgi
sed -i -e 's|/usr/local/dhcpstatus|%{_sysconfdir}|' %{buildroot}/%{_bindir}/%{name}
sed -i -e 's|/local||' %{buildroot}/%{_bindir}/%{name}
sed -i -e 's|/usr/local/dhcpstatus|%{_sysconfdir}|' %{buildroot}/var/www/cgi-bin/%{name}.cgi
sed -i -e 's|/etc/dhcpd\.leases|%{_localstatedir}/lib/dhcp/dhcpd.leases|' %{buildroot}/%{_sysconfdir}/dhcpstatus.ini

#(peroyvind) remove unpackaged files
rm -rf %{buildroot}%{_docdir}/%{name}_%{version}

%files 
%doc  INSTALL README LICENSE
%{perl_vendorlib}/dhcpstatus
%attr(755,root,root) /var/www/cgi-bin/*
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/*ini

