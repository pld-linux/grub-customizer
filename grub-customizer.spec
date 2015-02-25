Summary:	Graphical GRUB2 settings manager
Name:		grub-customizer
Version:	4.0.6
Release:	1
License:	GPL v3
Group:		X11/Applications
Source0:	https://launchpad.net/grub-customizer/4.0/%{version}/+download/%{name}_%{version}.tar.gz
# Source0-md5:	e4d76cd7cb6eb7ec03461e77db43bf34
Source1:	grub.cfg
URL:		https://launchpad.net/grub-customizer
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gtkmm3-devel
BuildRequires:	libarchive-devel
BuildRequires:	openssl-devel
Requires:	grub2
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
ExcludeArch:	%{arm}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Grub Customizer is a graphical interface to configure the grub2/burg
settings with focus on the individual list order - without losing the
dynamical behavior of grub.

The goal of this project is to create a complete and intuitive
graphical grub2/burg configuration interface. The main feature is the
boot entry list configuration - but not simply by modified the
grub.cfg: to keep the dynamical configuration, this application will
only edit the script order and generate proxies (script output
filter), if required.

%prep
%setup -q

%build
install -d build
cd build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/grub.cfg

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README changelog
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/grub.cfg
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%attr(755,root,root) %{_prefix}/lib/grub-customizer/grubcfg-proxy
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/polkit-1/actions/net.launchpad.danielrichter2007.pkexec.grub-customizer.policy
