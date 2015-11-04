Name:       chapeau-logos
Version:    1.3.1
Release:    1%{?dist}
Summary:    Icons and pictures

Group:      System Environment/Base
URL:        none_yet
Source0:    chapeau-logos-1.3.1.tar.bz2
#The KDE Logo is under a LGPL license (no version statement)
License:    GPLv2 and LGPLv2+
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

Requires: chapeau-packages
Obsoletes:  redhat-logos
Provides:   redhat-logos = %{version}-%{release}
Provides:   system-logos = %{version}-%{release}

Obsoletes:  fedora-logos
Obsoletes:  generic-logos
Conflicts:  anaconda-images <= 10
Conflicts:  redhat-artwork <= 5.0.5
# For _kde4_* macros:
BuildRequires: kde-filesystem
BuildRequires: hardlink
# For generating the EFI icon
BuildRequires: libicns-utils
Requires(post): coreutils


%description
This logos package for Chapeau! contains various image files which can be
used by the bootloader, anaconda, and other related tools. It is
used in the Fedora Remix, Chapeau as a replacement for the generic-logos
package.

%prep
%setup -c

%build
make

%install
rm -rf %{buildroot}

# should be ifarch i386
mkdir -p %{buildroot}/boot/grub
install -p -m 644 bootloader/splash.xpm.gz %{buildroot}/boot/grub/splash.xpm.gz
# end i386 bits


mkdir -p %{buildroot}%{_datadir}/firstboot/themes/generic
for i in firstboot/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/firstboot/themes/generic
done

mkdir -p %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora.icns %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora.vol %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora-media.vol  %{buildroot}%{_datadir}/pixmaps/bootloader

mkdir -p %{buildroot}%{_datadir}/pixmaps/splash
for i in gnome-splash/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/pixmaps/splash
done

mkdir -p %{buildroot}%{_datadir}/pixmaps
for i in pixmaps/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/pixmaps
done

mkdir -p %{buildroot}%{_kde4_iconsdir}/oxygen/48x48/apps/
install -p -m 644 icons/Fedora/48x48/apps/* %{buildroot}%{_kde4_iconsdir}/oxygen/48x48/apps/
mkdir -p %{buildroot}%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536
install -p -m 644 ksplash/SolarComet-kde.png %{buildroot}%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png

#mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge/
#for i in plymouth/charge/* ; do
#    install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge/
#done

# File or directory names do not count as trademark infringement
mkdir -p %{buildroot}%{_datadir}/icons/Fedora/48x48/apps/
mkdir -p %{buildroot}%{_datadir}/icons/Fedora/scalable/apps/
install -p -m 644 icons/Fedora/48x48/apps/* %{buildroot}%{_datadir}/icons/Fedora/48x48/apps/
install	-p -m 644 icons/Fedora/scalable/apps/* %{buildroot}%{_datadir}/icons/Fedora/scalable/apps/

(cd anaconda; make DESTDIR=%{buildroot} install)

# save some dup'd icons
/usr/sbin/hardlink -v %{buildroot}/

%post
touch --no-create %{_datadir}/icons/Fedora || :
touch --no-create %{_kde4_iconsdir}/oxygen ||:
#make default now
#/usr/sbin/plymout-set-default-theme -R charge
#/usr/bin/sed -i 's/^Theme=.*/Theme=charge/' /etc/plymouth/plymouthd.conf /usr/share/plymouth/plymouthd.defaults


%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/Fedora || :
touch --no-create %{_kde4_iconsdir}/oxygen ||:
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  if [ -f %{_datadir}/icons/Fedora/index.theme ]; then
    gtk-update-icon-cache --quiet %{_datadir}/icons/Fedora || :
  fi
  if [ -f %{_kde4_iconsdir}/Fedora-KDE/index.theme ]; then
    gtk-update-icon-cache --quiet %{_kde4_iconsdir}/Fedora-KDE/index.theme || :
  fi
fi
fi

%posttrans
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  if [ -f %{_datadir}/icons/Fedora/index.theme ]; then
    gtk-update-icon-cache --quiet %{_datadir}/icons/Fedora || :
  fi
  if [ -f %{_kde4_iconsdir}/oxygen/index.theme ]; then
    gtk-update-icon-cache --quiet %{_kde4_iconsdir}/oxygen/index.theme || :
  fi
fi


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING COPYING-kde-logo README
%{_datadir}/firstboot/themes/*
%{_datadir}/anaconda/boot/*
%{_datadir}/anaconda/pixmaps/*
%{_datadir}/icons/Fedora/*/apps/*
%{_datadir}/pixmaps/*
#%{_datadir}/plymouth/themes/charge/*
%{_kde4_appsdir}/ksplash/Themes/Leonidas/2048x1536/logo.png
%{_kde4_iconsdir}/oxygen/
# should be ifarch i386
/boot/grub/splash.xpm.gz
# end i386 bits

%changelog
* Tue Nov 03 2015 Vince Pooley <vince@chapeaulinux.org> - 1.3.1
- Changed %setup macro option to 'c'

* Mon Jun 30 2014 Vince Pooley <vince@chapeaulinux.org> - 1.3
- Removed pixmaps/poweredby.png to remove a conflict with
- fedora-httpd-logos package

* Fri Feb 28 2014 Vince Pooley <vince@chapeaulinux.org> - 1.2
- Removed Plymouth charge theme files to remove a confilct

* Mon Jan 13 2014 Vince Pooley <vince@chapeaulinux.org> - 1.1
- Minor change to pull in the Chapeau meta-package (as this is
- currently the only package in the Chapeau repo) and to
- change the name of the included 'chapeau' plymouth theme to
- 'charge', a copy of the same theme will be repackaged in the
- 'plymouth-theme-chapeau' package. The plymouth theme is also
- changed so the progress bar is removed by default.

