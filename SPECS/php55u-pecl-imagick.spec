%global pecl_name  imagick
%global real_name php-pecl-imagick
%global php_base php55u
%global ini_name  40-%{pecl_name}.ini

Summary: Provides a wrapper to the ImageMagick library
Name: %{php_base}-pecl-%{pecl_name}
Version: 3.3.0
Release: 2.ius%{?dist}
License: PHP
Group: Development/Libraries
Source0: http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1: %{pecl_name}.ini
URL: http://pecl.php.net/package/%{pecl_name}
BuildRequires: %{php_base}-pear
BuildRequires: %{php_base}-devel
BuildRequires: ImageMagick-devel >= 6.2.4
Requires(post): %{php_base}-pear
Requires(postun): %{php_base}-pear
Requires: %{php_base}(api) = %{php_core_api}
Requires: %{php_base}(zend-abi) = %{php_zend_api}

Provides: php-%{pecl_name} = %{version}
Provides: php-%{pecl_name}%{?_isa} = %{version}
Provides: php-pecl(%{pecl_name}) = %{version}
Provides: php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides: %{php_base}-%{pecl_name} = %{version}
Provides: %{php_base}-%{pecl_name}%{?_isa} = %{version}
Provides: %{php_base}-pecl(%{pecl_name}) = %{version}
Provides: %{php_base}-pecl(%{pecl_name})%{?_isa} = %{version}

Provides: %{real_name} = %{version}
Conflicts: %{real_name} < %{version}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
%{pecl_name} is a native php extension to create and modify images using the
ImageMagick API. This extension requires ImageMagick version 6.2.4+ and
PHP 5.1.3+.

IMPORTANT: Version 2.x API is not compatible with earlier versions.


%prep
%setup -q -n %{pecl_name}-%{version}


%build
phpize
%{configure} --with-%{pecl_name}
%{__make}


%install
%{__make} install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -m 0755 -d %{buildroot}%{pecl_xmldir}
install -m 0664 package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml
install -d %{buildroot}%{_sysconfdir}/php.d/
install -m 0664 %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/%{ini_name}

%{__rm} -rf %{buildroot}/%{_includedir}/php/ext/%{pecl_name}/


%check
# simple module load test
php --no-php-ini \
    --define extension_dir=%{buildroot}%{php_extdir} \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%post
%if 0%{?pecl_install:1}
%{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml
%endif


%postun
%if 0%{?pecl_uninstall:1}
if [ "$1" -eq "0" ]; then
  %{pecl_uninstall} %{pecl_name}
fi
%endif


%files
%doc examples CREDITS
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{pecl_name}.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php.d/%{ini_name}


%changelog
* Wed Feb 17 2016 Carl George <carl.george@rackspace.com> - 3.3.0-2.ius
- Explicitly require %%{php_base}(api) and %%{php_base}(zend-abi)
- Manually filter provides only when needed

* Mon Dec 07 2015 Ben Harper <ben.harper@rackspace.com> - 3.3.0-1.ius
- Latest sources from upstream
- remove TODO and INSTALL from %%files

* Tue Jul 28 2015 Ben Harper <ben.harper@rackspace.com> - 3.1.2-5.ius
- rebuild for updated ImageMagick in EL 6.7

* Fri Oct 10 2014 Carl George <carl.george@rackspace.com> - 3.1.2-4.ius
- Directly require the correct pear package, not /usr/bin/pecl
- Conflict with stock package
- Use same provides as stock package

* Fri Oct 03 2014 Carl George <carl.george@rackspace.com> - 3.1.2-3.ius
- Add numerical prefix to extension configuration file
- Add filter to avoid private-shared-object-provides
- Add minimal %%check
- Remove unneeded header files

* Thu Apr 10 2014 Ben Harper <ben.harper@rackspace.com> - 3.1.2-2.ius
- porting from php54-pecl-imagick

* Wed Sep 25 2013 Ben Harper <ben.harper@rackspace.com> - 3.1.2-1.ius
- Latest sources from upstream

* Mon Sep 23 2013 Ben Harper <ben.harper@rackspace.com> - 3.1.1-1.ius
- latest release, 3.1.1

* Tue Aug 21 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.1.0-RC1.2.ius
- Rebuilding against php54-5.4.6-2.ius as it is now using bundled PCRE.

* Fri May 11 2012 Dustin Henry Offutt <dustin.offutt@rackspace.com> 3.1.0-RC1.1.ius
- Building for php54 and imagick 3.1.0RC1
- Add define rc_version, add rc_version to Release definition, Source0 path, BuildRoot path, and setup line

* Fri Aug 19 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.0.1-3.ius
- Rebuilding

* Tue Feb 01 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 3.0.1-2.ius
- Removed Obsoletes: php53*

* Thu Dec 16 2010 BJ Dierkes <wdierkes@rackspace.com> - 3.0.1-1.ius
- Latest sources from upstream.  Full changelog available at:
  http://pecl.php.net/package-changelog.php?package=imagick&release=3.0.1
- Renaming package as php53u-pecl-imagick, Resolves LP#691755
- Rebuild against php53u-5.3.4
- BuildRequires: php53u-cli

* Tue Jul 27 2010 BJ Dierkes <wdierkes@rackspace.com> - 3.0.0-1.ius
- Latest sources from upstream
- Porting over to php53 (5.3.3) 

* Thu Dec 17 2009 BJ Dierkes <wdierkes@rackspace.com> - 2.3.0-1.ius
- Rebuilding for IUS Community Project
- Latest sources from upstream
- Building against php52-5.2.12, php52-pear

* Sun Jan 11 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.2.1-3
- All modifications in this release inspired by Fedora review by Remi Collet.
- Add versions to BR for php-devel and ImageMagick-devel
- Remove -n option from %%setup which was excessive with -c
- Module install/uninstall actions surround with %%if 0%{?pecl_(un)?install:1} ... %%endif
- Add Provides: php-pecl(%%peclName) = %%{version}

* Sat Jan 3 2009 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.2.1-2
- License changed to PHP (thanks to Remi Collet)
- Add -c flag to %%setup (Remi Collet)
  And accordingly it "cd %%peclName-%%{version}" in %%build and %%install steps.
- Add (from php-pear template)
  Requires(post): %%{__pecl}
  Requires(postun): %%{__pecl}
- Borrow from Remi Collet php-api/abi requirements.
- Use macroses: (Remi Collet)
  %%pecl_install instead of direct "pear install --soft --nobuild --register-only"
  %%pecl_uninstall instead of pear "uninstall --nodeps --ignore-errors --register-only"
- %%doc examples/{polygon.php,captcha.php,thumbnail.php,watermark.php} replaced by %%doc examples (Remi Collet)
- Change few patchs to macroses: (Remi Collet)
  %%{_libdir}/php/modules - replaced by %%{php_extdir}
  %%{xmldir} - by %%{pecl_xmldir}
- Remove defines of xmldir, peardir.
- Add 3 recommended macroses from doc http://fedoraproject.org/wiki/Packaging/PHP : php_apiver, __pecl, php_extdir

* Sat Dec 20 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.2.1-1
- Step to version 2.2.1
- As prepare to push it into Fedora:
 - Change release to 1%%{?dist}
 - Set setup quiet
 - Escape all %% in changelog section
 - Delete dot from summary
 - License change from real "PHP License" to BSD (by example with php-peck-phar and php-pecl-xdebug)
- %%defattr(-,root,root,-) changed to %%defattr(-,root,root,-)

* Mon May 12 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] spb [ dOt.] su> - 2.2.0b2-0.Hu.0
- Step to version 2.2.0b2
- %%define peclName imagick and replece to it all direct appearances.

* Thu Mar 6 2008 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 2.1.1RC1-0.Hu.0
- Steep to version 2.1.1RC1 -0.Hu.0
- Add Hu-part and %%{?dist} into Release
- Add BuildRequires: ImageMagick-devel

* Fri Oct 12 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 2.0.0RC1
- Global rename from php-pear-imagick to php-pecl-imagick. This is more correct.

* Wed Aug 22 2007 Pavel Alexeev <Pahan [ at ] Hubbitus [ DOT ] info> - 2.0.0RC1
- Initial release. (Re)Written from generated (pecl make-rpm-spec)
