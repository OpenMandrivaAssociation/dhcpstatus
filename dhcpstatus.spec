%define	name	dhcpstatus
%define	version	0.60
%define	release	%mkrel 15

Summary:	Dhcp IP status cgi
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		%{name}_%{version}.tar.bz2
Source1:	%{name}_%{version}.patch
#Source2:	%{name}_%{version}-lib.patch.bz2
License:	GPL
URL:		http://dhcpstatus.sourceforge.net
BuildRoot:	%{_tmppath}/build-%{name}_%{version}
Group:		Monitoring
Requires:	dhcp-server perl-CGI
BuildArch:	noarch

%define _requires_exceptions perl(dhcpstatus::Dhcpstatus_env)\\|perl(dhcpstatus::Display)\\|perl(dhcpstatus::Formatted_text)\\|perl(dhcpstatus::Lease)\\|perl(dhcpstatus::Line_print)\\|perl(dhcpstatus::Pool)\\|perl(dhcpstatus::Subnet)\\|perl(dhcpstatus::common)\\|perl(dhcpstatus::dhcpstatus)\\|perl(dhcpstatus::dhcpstatus_cgi)\\|perl(dhcpstatus::dhcpstatus_cmd)\\|perl(dhcpstatus::dhcpstatus_subnet)\\|perl(dhcpstatus::dhcpstatus_subnet_cgi)\\|perl(dhcpstatus::dhcpstatus_subnet_cmd)\\|perl(dhcpstatus::display_html)\\|perl(dhcpstatus::display_line)\\|perl(dhcpstatus::iptools)  


%description
DHCP-Status is basically two Perl CGI scripts that provide an overall picture
of the information contained in the dhcpd.conf and dhcpd.leases files that
are used by ISC's DHCP server, DHCPD.

%prep
%setup -q -n %{name}_%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%perl_vendorlib/%{name}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}_%{version}
mkdir -p $RPM_BUILD_ROOT/var/www/cgi-bin
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/
tar xf $RPM_BUILD_DIR/%{name}_%{version}/libraries.tar
# TODO: Fix Apply patch 
bzcat %{SOURCE1} | patch -p0
#bzcat %{SOURCE2} | patch -p0

cp -a $RPM_BUILD_DIR/%{name}_%{version}/%{name}/*.pm $RPM_BUILD_ROOT/%perl_vendorlib/%{name}
cp -a $RPM_BUILD_DIR/%{name}_%{version}/{README,INSTALL,LICENSE} $RPM_BUILD_ROOT%{_docdir}/%{name}_%{version}
cp -a $RPM_BUILD_DIR/%{name}_%{version}/scripts/*.cgi $RPM_BUILD_ROOT/var/www/cgi-bin
cp -a $RPM_BUILD_DIR/%{name}_%{version}/scripts/%{name} $RPM_BUILD_ROOT/%{_bindir}
cp -a $RPM_BUILD_DIR/%{name}_%{version}/*.ini $RPM_BUILD_ROOT/%{_sysconfdir}/
perl -p -i -e 's|/etc/dhcpd\.leases|%{_localstatedir}/lib/dhcp/dhcpd.leases|' $RPM_BUILD_ROOT/var/www/cgi-bin/%{name}.cgi
perl -p -i -e 's|/usr/local/dhcpstatus|%{_sysconfdir}|' $RPM_BUILD_ROOT/%{_bindir}/%{name}
perl -p -i -e 's|/local||' $RPM_BUILD_ROOT/%{_bindir}/%{name}
perl -p -i -e 's|/usr/local/dhcpstatus|%{_sysconfdir}|' $RPM_BUILD_ROOT/var/www/cgi-bin/%{name}.cgi
perl -p -i -e 's|/etc/dhcpd\.leases|%{_localstatedir}/lib/dhcp/dhcpd.leases|' $RPM_BUILD_ROOT/%{_sysconfdir}/dhcpstatus.ini

#(peroyvind) remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}_%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc  INSTALL README LICENSE
%{perl_vendorlib}/dhcpstatus
%attr(755,root,root) /var/www/cgi-bin/*
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/*ini

