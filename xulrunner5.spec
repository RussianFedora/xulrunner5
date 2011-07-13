%global shortname         xulrunner

# Minimal required versions
%global nspr_version 4.8.7
%global nss_version 3.12.9
%global cairo_version 1.10.0
%global freetype_version 2.1.9
%global sqlite_version 3.7.5
%global libnotify_version 0.7.0
%global lcms_version 1.18

# gecko_dir_ver should be set to the version in our directory names
# alpha_version should be set to the alpha number if using an alpha, 0 otherwise
# beta_version  should be set to the beta number if using a beta, 0 otherwise
# rc_version    should be set to the RC number if using an RC, 0 otherwise
%global gecko_dir_ver 5
%global alpha_version 0
%global beta_version  0
%global rc_version    0

%global mozappdir         %{_libdir}/%{shortname}-%{gecko_dir_ver}
%global tarballdir        mozilla-release
%global gre_dir           %{_sysconfdir}/gre.d

# crash reporter and out-of-process-plugins work only on x86/x86_64
%ifarch %{ix86} x86_64
%global enable_mozilla_crashreporter 1
%global moz_out_of_process_plugins   1
%else
%global enable_mozilla_crashreporter 0
%global moz_out_of_process_plugins   0
%endif

%ifarch x86_64
%global gre_conf_file gre5-64.conf
%else
%global gre_conf_file gre5.conf
%endif


# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)

%if %{alpha_version} > 0
%global pre_version a%{alpha_version}
%global pre_name    alpha%{alpha_version}
%endif
%if %{beta_version} > 0
%global pre_version b%{beta_version}
%global pre_name    beta%{beta_version}
%endif
%if %{rc_version} > 0
%global pre_version rc%{rc_version}
%global pre_name    rc%{rc_version}
%endif
%if %{defined pre_version}
%global gecko_verrel %{expand:%%{version}}-%{pre_name}
%global pre_tag .%{pre_version}
%else
%global gecko_verrel %{expand:%%{version}}-1
%endif

Summary:        XUL Runtime for Gecko Applications
Name:           %{shortname}5
Version:        5.0
Release:        1%{?pre_tag}%{?dist}
URL:            http://developer.mozilla.org/En/XULRunner
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
# You can get sources at ftp://ftp.mozilla.org/pub/firefox/releases/%{version}%{?pretag}/source
#Source0:        %{shortname}-%{version}%{?pretag}.source.tar.bz2
Source0:        ftp://ftp.mozilla.org/pub/firefox/releases/5.0/source/firefox-%{version}.source.tar.bz2
Source10:       %{shortname}-mozconfig
Source11:       %{shortname}-mozconfig-debuginfo
Source12:       %{shortname}-redhat-default-prefs.js
Source21:       %{shortname}.sh.in

# build patches
Patch0:         xulrunner-version.patch
Patch1:         mozilla-build.patch
Patch9:         mozilla-build-sbrk.patch
Patch13:        xulrunner-2.0-secondary-jit.patch
Patch14:        xulrunner-2.0-chromium-types.patch
Patch15:        firefox-5.0-xulstub.patch
%if 0%{?fedora} <= 15 || 0%{?rhel} > 5
Patch16:        add-gtkmozembed.patch
%endif
%if 0%{?fedora} > 15
Patch17:        xulrunner-5.0-curl.patch
%endif

# Fedora specific patches
Patch20:        mozilla-193-pkgconfig.patch
Patch21:        mozilla-libjpeg-turbo.patch
Patch23:        wmclass.patch
Patch24:        crashreporter-remove-static.patch

# Upstream patches
Patch32:        firefox-4.0-moz-app-launcher.patch
Patch33:        firefox-4.0-gnome3.patch
Patch34:        xulrunner-2.0-network-link-service.patch
Patch35:        xulrunner-2.0-NetworkManager09.patch
Patch36:        xulrunner-omnijar-5.patch

# cairo-freeworld patches

Patch41: cairo-respect-fontconfig.patch
Patch42: cairo-1.10.0-buggy_gradients.patch

# ---------------------------------------------------

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%if 0%{?fedora} >= 13 || 0%{?rhel} > 5
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
%endif
%if 0%{?fedora} >= 15
BuildRequires:  cairo-devel >= %{cairo_version}
%endif
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
%if 0%{?fedora} >= 11 || 0%{?rhel} > 5
BuildRequires:  hunspell-devel
%endif
%if 0%{?fedora} >= 15
BuildRequires:  sqlite-devel >= %{sqlite_version}
%endif
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libnotify-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  lcms-devel >= %{lcms_version}
BuildRequires:  yasm
%ifarch %{ix86} x86_64
BuildRequires:  wireless-tools-devel
%endif
%if 0%{?fedora} >= 13
BuildRequires:  libcurl-devel
BuildRequires:  libvpx-devel
%endif

Requires:       mozilla-filesystem
%if 0%{?fedora} >= 13
Requires:       nspr >= %{nspr_version}
Requires:       nss >= %{nss_version}
%endif
%if 0%{?fedora} >= 15
Requires:       sqlite >= %{sqlite_build_version}
%endif
Provides:       gecko-libs = %{gecko_verrel}
Provides:       gecko-libs%{?_isa} = %{gecko_verrel}


%description
XULRunner is a Mozilla runtime package that can be used to bootstrap XUL+XPCOM
applications that are as rich as Firefox and Thunderbird. It provides mechanisms
for installing, upgrading, and uninstalling these applications. XULRunner also
provides libxul, a solution which allows the embedding of Mozilla technologies
in other projects and products.

%package devel
Summary: Development files for Gecko
Group: Development/Libraries
Obsoletes: mozilla-devel < 1.9
Obsoletes: firefox-devel < 2.1
Obsoletes: xulrunner-devel-unstable
Provides: gecko-devel = %{gecko_verrel}
Provides: gecko-devel%{?_isa} = %{gecko_verrel}
Provides: gecko-devel-unstable = %{gecko_verrel}
Provides: gecko-devel-unstable%{?_isa} = %{gecko_verrel}

Requires: %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} >= 13 || 0%{?rhel} > 5
Requires: nspr-devel >= %{nspr_version}
Requires: nss-devel >= %{nss_version}
%endif
%if 0%{?fedora} >= 15
Requires: cairo-devel >= %{cairo_version}
%endif
Requires: libjpeg-devel
Requires: zip
Requires: bzip2-devel
Requires: zlib-devel
Requires: libIDL-devel
Requires: gtk2-devel
Requires: krb5-devel
Requires: pango-devel
Requires: freetype-devel >= %{freetype_version}
Requires: libXt-devel
Requires: libXrender-devel
%if 0%{?fedora} >= 11
Requires: hunspell-devel
%endif
Requires: sqlite-devel
Requires: startup-notification-devel
Requires: alsa-lib-devel
Requires: libnotify-devel
Requires: mesa-libGL-devel
Requires: lcms-devel
Requires: yasm
%ifarch %{ix86} x86_64
Requires: wireless-tools-devel
%endif

%description devel
This package contains the libraries amd header files that are needed
for writing XUL+XPCOM applications with Mozilla XULRunner and Gecko.

%if %{enable_mozilla_crashreporter}
%global moz_debug_prefix %{_prefix}/lib/debug
%global moz_debug_dir %{moz_debug_prefix}%{mozappdir}
%global uname_m %(uname -m)
%global symbols_file_name %{shortname}-%{version}.en-US.%{_os}-%{uname_m}.crashreporter-symbols.zip
%global symbols_file_path %{moz_debug_dir}/%{symbols_file_name}
%global _find_debuginfo_opts -p %{symbols_file_path} -o debugcrashreporter.list
%global crashreporter_pkg_name mozilla-crashreporter-%{name}-debuginfo
%package -n %{crashreporter_pkg_name}
Summary: Debugging symbols used by Mozilla's crash reporter servers
Group: Development/Debug
%description -n %{crashreporter_pkg_name}
This package provides debug information for XULRunner, for use by
Mozilla's crash reporter servers.  If you are trying to locally
debug %{name}, you want to install %{name}-debuginfo instead.
%files -n %{crashreporter_pkg_name} -f debugcrashreporter.list
%defattr(-,root,root)
%endif


#---------------------------------------------------------------------

%prep
echo TARGET = %{name}-%{version}-%{release}%{?dist}
%setup -q -c
cd %{tarballdir}

sed -e 's/__RPM_VERSION_INTERNAL__/%{gecko_dir_ver}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch

%patch1  -p2 -b .build
%patch9  -p2 -b .sbrk
%patch13 -p2 -b .secondary-jit
%patch14 -p2 -b .chromium-types
%patch15 -p1 -R -b .xulstub
%if 0%{?fedora} <= 15 || 0%{?rhel} > 5
%patch16 -p2 -b .gtkmozembed
%endif
%if 0%{?fedora} > 15
%patch17 -p2 -b .curl
%endif

%patch20 -p2 -b .pk
%if 0%{?fedora} >= 14
%patch21 -p2 -b .jpeg-turbo
%endif
%patch23 -p1 -b .wmclass
%patch24 -p1 -b .static

%patch32 -p1 -b .moz-app-launcher
%patch33 -p1 -b .gnome3
%patch34 -p2 -b .network-link-service
%patch35 -p1 -b .NetworkManager09
%patch36 -p2 -b .omnijar

pushd gfx/cairo/cairo
%patch41 -p1 -b .respect-fontconfig
%patch42 -p1 -b .buggy_gradients
popd

%{__rm} -f .mozconfig
%{__cat} %{SOURCE10} \
%if 0%{?fedora} < 15 || 0%{?rhel} > 5
  | grep -v enable-system-sqlite   \
%endif
%if 0%{?fedora} < 13 || 0%{?rhel} > 5
  | grep -v with-system-nspr       \
  | grep -v with-system-nss        \
%endif
%if 0%{?fedora} < 11
  | grep -v enable-system-hunspell \
%endif
%if 0%{?fedora} < 15 || 0%{?rhel} > 5
  | grep -v enable-system-cairo    \
%endif
%ifarch %{ix86} x86_64
  | grep -v disable-necko-wifi     \
%endif
%if 0%{?fedora} < 13 || 0%{?rhel} > 5
  | grep -v with-system-libvpx     \
%endif
  | tee .mozconfig

%if %{enable_mozilla_crashreporter}
%{__cat} %{SOURCE11} >> .mozconfig
%endif

echo "ac_add_options --enable-system-lcms" >> .mozconfig

%if !%{?moz_out_of_process_plugins}
echo "ac_add_options --disable-ipc" >> .mozconfig
%endif

# Upstream bug filed without resolution
# for now make sure jit is not enabled on sparc64
%ifarch sparc64
echo "ac_add_options --disable-tracejit" >> .mozconfig
%endif

%if 0%{?fedora} < 14 || 0%{?rhel} > 5
echo "ac_add_options --disable-libjpeg-turbo" >> .mozconfig
%endif

#---------------------------------------------------------------------

%build
%if 0%{?fedora} >= 15
# Do not proceed with build if the sqlite require would be broken:
# make sure the minimum requirement is non-empty, ...
sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
# ... and that major number of the computed build-time version matches:
case "%{sqlite_build_version}" in
  "$sqlite_version"*) ;;
  *) exit 1 ;;
esac
%endif

cd %{tarballdir}

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
# 
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS -fpermissive" | \
                      %{__sed} -e 's/-Wall//' -e 's/-fexceptions/-fno-exceptions/g')
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
%endif

export LDFLAGS="-Wl,-rpath,%{mozappdir}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
#cd %{moz_objdir}
make buildsymbols
%endif

#---------------------------------------------------------------------

%install
cd %{tarballdir}
%{__rm} -rf $RPM_BUILD_ROOT

INTERNAL_APP_SDK_NAME=%{shortname}-sdk-%{gecko_dir_ver}
MOZ_APP_SDK_DIR=%{_libdir}/${INTERNAL_APP_SDK_NAME}

# set up our prefs before install, so it gets pulled in to omni.jar
%{__cp} -p %{SOURCE12} dist/bin/defaults/pref/all-redhat.js

DESTDIR=$RPM_BUILD_ROOT make install

%{__mkdir_p} $RPM_BUILD_ROOT/%{mozappdir} \
             $RPM_BUILD_ROOT%{_datadir}/idl/${INTERNAL_APP_SDK_NAME} \
             $RPM_BUILD_ROOT%{_includedir}/${INTERNAL_APP_SDK_NAME}
%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

# Start script install
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/%{shortname}
%{__cat} %{SOURCE21} | %{__sed} -e 's,XULRUNNER_VERSION,%{gecko_dir_ver},g' > \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

%{__rm} -f $RPM_BUILD_ROOT%{mozappdir}/%{shortname}-config

# Prepare our devel package
%{__mkdir_p} $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datadir}/idl/${INTERNAL_APP_SDK_NAME}
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

%{__cp} -rL dist/include/* \
  $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}

# Copy pc files (for compatibility with 1.9.1)
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-unstable.pc
%{__cp} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding.pc \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/libxul-embedding-unstable.pc

# Fix multilib devel conflicts...
function install_file() {
genheader=$*
mv ${genheader}.h ${genheader}%{__isa_bits}.h
cat > ${genheader}.h << EOF
/* This file exists to fix multilib conflicts */
#if defined(__x86_64__) || defined(__ia64__) || defined(__s390x__) || defined(__powerpc64__) || (defined(__sparc__) && defined(__arch64__))
#include "${genheader}64.h"
#else
#include "${genheader}32.h"
#endif
EOF
}

pushd $RPM_BUILD_ROOT/%{_includedir}/${INTERNAL_APP_SDK_NAME}
install_file "mozilla-config"
install_file "jsautocfg"
install_file "js-config"
popd

%{__install} -p -c -m 755 dist/bin/xpcshell \
  dist/bin/xpidl \
  dist/bin/xpt_dump \
  dist/bin/xpt_link \
  $RPM_BUILD_ROOT/%{mozappdir}

%if 0%{?fedora} < 13 || 0%{?rhel} > 5
%{__install} -D -p -m 755 \
   dist/sdk/bin/nspr-config \
   $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/bin/nspr-config
%endif

%{__rm} -rf $RPM_BUILD_ROOT/%{_includedir}/%{shortname}-%{gecko_dir_ver}
%{__rm} -rf $RPM_BUILD_ROOT/%{_datadir}/idl/%{shortname}-%{gecko_dir_ver}

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/include
ln -s  %{_includedir}/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/include

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/idl
ln -s  %{_datadir}/idl/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/idl

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/include
ln -s  %{_includedir}/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/include

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/idl
ln -s  %{_datadir}/idl/${INTERNAL_APP_SDK_NAME} \
       $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/idl

find $RPM_BUILD_ROOT/%{_includedir} -type f -name "*.h" | xargs chmod 644
find $RPM_BUILD_ROOT/%{_datadir}/idl -type f -name "*.idl" | xargs chmod 644

%{__rm} -rf $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/lib/*.so
pushd $RPM_BUILD_ROOT%{mozappdir}
for i in *.so; do
    ln -s %{mozappdir}/$i $RPM_BUILD_ROOT${MOZ_APP_SDK_DIR}/sdk/lib/$i
done
popd

# GRE stuff
MOZILLA_GECKO_VERSION=`./config/milestone.pl --topsrcdir=.`
%{__mv} $RPM_BUILD_ROOT%{gre_dir}/$MOZILLA_GECKO_VERSION".system.conf" \
        $RPM_BUILD_ROOT%{gre_dir}/%{gre_conf_file}
chmod 644 $RPM_BUILD_ROOT%{gre_dir}/%{gre_conf_file}

# Library path
LD_SO_CONF_D=%{_sysconfdir}/ld.so.conf.d
LD_CONF_FILE=xulrunner-%{__isa_bits}.conf

%if %{name} == %{shortname}
%{__mkdir_p} ${RPM_BUILD_ROOT}${LD_SO_CONF_D}
%{__cat} > ${RPM_BUILD_ROOT}${LD_SO_CONF_D}/${LD_CONF_FILE} << EOF
%{mozappdir}
EOF
%endif

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT%{mozappdir}

# Use the system hunspell dictionaries
%{__rm} -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/components
touch $RPM_BUILD_ROOT%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{mozappdir}/components/xpti.dat

# Add debuginfo for crash-stats.mozilla.com 
%if %{enable_mozilla_crashreporter}
%{__mkdir_p} $RPM_BUILD_ROOT/%{moz_debug_dir}
%{__cp} dist/%{symbols_file_name} $RPM_BUILD_ROOT/%{moz_debug_dir}
%endif

# Remi : this appears on Fedora <= 13
%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/*.chk


#---------------------------------------------------------------------

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%if %{name} == %{shortname}
%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
fi
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%dir %{_sysconfdir}/gre.d
%{_sysconfdir}/gre.d/gre*.conf
%dir %{mozappdir}
%doc %attr(644, root, root) %{mozappdir}/LICENSE
%doc %attr(644, root, root) %{mozappdir}/README.txt
%{mozappdir}/chrome
%{mozappdir}/chrome.manifest
%{mozappdir}/dictionaries
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.manifest
%dir %{mozappdir}/icons
%attr(644, root, root) %{mozappdir}/icons/*
%{mozappdir}/omni.jar
%{mozappdir}/plugins
%{mozappdir}/*.so
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/run-mozilla.sh
%{mozappdir}/xulrunner
%{mozappdir}/xulrunner-bin
%{mozappdir}/xulrunner-stub
%{mozappdir}/platform.ini
%{mozappdir}/dependentlibs.list
%if %{name} == %{shortname}
%{_sysconfdir}/ld.so.conf.d/xulrunner*.conf
%endif
%if %{?moz_out_of_process_plugins}
%{mozappdir}/plugin-container
%endif

%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%endif

%files devel
%defattr(-,root,root,-)
%{_datadir}/idl/%{shortname}*%{gecko_dir_ver}
%{_includedir}/%{shortname}*%{gecko_dir_ver}
%{_libdir}/%{shortname}-sdk-*/
%{_libdir}/pkgconfig/*.pc
%{mozappdir}/xpcshell
%{mozappdir}/xpidl
%{mozappdir}/xpt_dump
%{mozappdir}/xpt_link

#---------------------------------------------------------------------

%changelog
* Fri Jun 24 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-1
- sync with f15/rawhide
- update to 5.0 finale

* Tue Jun 24 2011 Martin Stransky <stransky@redhat.com> 5.0-3
- libCurl build fix

* Wed Jun 22 2011 Martin Stransky <stransky@redhat.com> 5.0-2
- Reverted mozbz#648156 - Remove gtkmozembed

* Tue Jun 21 2011 Martin Stransky <stransky@redhat.com> 5.0-1
- 5.0

* Thu Jun 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-0.6.build1
- Update to 5.0 build 1 candidate

* Wed Jun 15 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-0.4.beta7.build1
- Update to 5.0 Beta 7 build 1 candidate

* Tue Jun 14 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-0.2.beta6.build1
- Update to 5.0 Beta 6 build 1 candidate

* Sun Jun 12 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-0.1.b5.build1
- use patch from spot
- Update to 5.0b5 build1

* Wed Jun  1 2011 Tom Callaway <spot@fedoraproject.org> - 5.0-0.1.b3
- firefox5, xulrunner5

* Wed Jun  1 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.0-0.1.b3.build1
- xulrunner5

* Sun Apr 17 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-0.1.build1
- Update to 2.0.1 build1 candidate

* Sun Apr 10 2011 Christopher Aillon <caillon@redhat.com> - 2.0-3
- Fix offline status issue on version upgrades
- Fix a hang with 20+ extensions

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> - 2.0-2
- Fix SIGABRT in X_CloseDevice: XI_BadDevice
- Updates for NetworkManager 0.9
- Updates for GNOME 3

* Tue Mar 22 2011 Christopher Aillon <caillon@redhat.com> - 2.0-1
- 2.0

* Tue Mar 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-1
- Update to 2.0

* Sat Mar 19 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.26.rc2
- Update to 2.0 RC2

* Fri Mar 18 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.28
- Update to 2.0 RC2

* Thu Mar 17 2011 Jan Horak <jhorak@redhat.com> - 2.0-0.27
- Disabled gnomevfs
- Enabled gio
- Build with system libvpx

* Thu Mar 10 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.25.rc1
- Update to 2.0 RC1

* Wed Mar  9 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.26
- Update to 2.0 RC 1

* Sat Mar 05 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.24.rc1.build1
- Update to 2.0 RC1 build1 candidate

* Mon Feb 28 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.23.beta12
- sync with rawhide
- update to 2.0 Beta12

* Sun Feb 27 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.25
- Make Firefox's User-Agent string match upstream's

* Sat Feb 26 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.24
- Switch to using the omni chrome file format

* Fri Feb 25 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.23
- Update to 2.0 Beta 12

* Wed Feb 23 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.22.beta12.build1
- sync with rawhide
- update to 2.0 Beta12 build1 candidate

* Sun Feb 13 2011 Dennis Gilmore <dennis@ausil.us> 2.0-0.22
- disable nanojit on sparc64 its not supported and doesnt get automatically switched off

* Thu Feb 10 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.21
- Also provide arch-agnostic versions of gecko virtual provides

* Thu Feb 10 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.20
- Introduce better versioning for our gecko virtual provides
- Now, the gecko-libs and gecko-devel virtual provides will be pinned
  to an individual Gecko release, so packages can do things like
    Requires: gecko-libs = 2.0-beta11
    BuildRequires: gecko-libs = 2.0-beta11
- Final releases will be pinned to e.g. 2.0-1 regardless of %%{release}
- Also, make sure those virtual provides are arch-specific

* Wed Feb 09 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.21.beta11
- Update to 2.0 Beta 11

* Tue Feb  8 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.19
- Update to 2.0 Beta 11

* Fri Feb 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.20.beta11.build3
- 2.0b11 build3 candidate (using firefox sources)

* Thu Feb 03 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.19.beta11.build2
- 2.0b11 build2 candidate (using firefox sources)

* Tue Feb 01 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.0-0.18.beta10
- rename to xulrunner2
- merge most changes from spot
- backport to remi repo

* Wed Jan 26 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.18
- Fix issue with popup windows showing in the wrong place

* Tue Jan 25 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.17
- Update to 2.0 Beta 10

* Fri Jan 21 2011 Dan Horák <dan[at]danny.cz> - 2.0-0.16.b9
- updated the 64bit-big-endian patch (bmo#627664)
- added fix for build with --disable-methodjit (bmo#623277)

* Fri Jan 14 2011 Christopher Aillon <caillon@redhat.com> 2.0-0.15.b9
- Update to 2.0 Beta 9

* Thu Jan 11 2011 Tom Callaway <spot@fedoraproject.org> 2.0-0.14.b8
- enable system sqlite (see https://fedorahosted.org/fpc/ticket/34)

* Thu Dec 23 2010 Martin Stransky <stransky@redhat.com> 2.0-0.13.b8
- reverted fix for rhbz#658471

* Wed Dec 22 2010 Dan Horák <dan[at]danny.cz> - 2.0-0.11.b8
- updated the 64bit-big-endian patch

* Tue Dec 21 2010 Martin Stransky <stransky@redhat.com> 2.0-0.11.b8
- enable url-classifier and jar format for chrome files

* Tue Dec 21 2010 Martin Stransky <stransky@redhat.com> 2.0-0.10.b8
- Update to 2.0b8

* Mon Dec 20 2010 Martin Stransky <stransky@redhat.com> 2.0-0.9.b8
- removed unused library path (rhbz#658471)

* Fri Dec 17 2010 Dan Horák <dan[at]danny.cz> - 2.0-0.8.b7
- disable the crash reporter on non-x86 arches
- add sparc64 as 64-bit arch

* Tue Dec 14 2010 Jan Horak <jhorak@redhat.com> - 2.0-0.7.b7
- Enable mozilla crash reporter

* Thu Nov 11 2010 Dan Horák <dan[at]danny.cz> - 2.0-0.6.b7
- The s390 patch is not needed anymore

* Thu Nov 11 2010 Jan Horak <jhorak@redhat.com> - 2.0-0.5.b7
- Update to 2.0b7

* Thu Nov 4 2010 Christopher Aillon <caillon@redhat.com> 2.0-0.4.b6
- Ensure that WM_CLASS matches the desktop file

* Wed Nov 3 2010 Martin Stransky <stransky@redhat.com> 2.0-0.3.b6
- Libnotify rebuild (rhbz#649071)

* Wed Sep 29 2010 jkeating - 2.0-0.2b6
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Martin Stransky <stransky@redhat.com> 2.0-0.1.b6
- Update to 2.0b6


