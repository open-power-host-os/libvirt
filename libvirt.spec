# -*- rpm-spec -*-

ExclusiveArch: ppc64 x86_64

# If neither fedora nor rhel was defined, try to guess them from %{dist}
%if !0%{?rhel} && !0%{?fedora}
%{expand:%(echo "%{?dist}" | \
  sed -ne 's/^\.el\([0-9]\+\).*/%%define rhel \1/p')}
%{expand:%(echo "%{?dist}" | \
  sed -ne 's/^\.fc\?\([0-9]\+\).*/%%define fedora \1/p')}
%endif

# Default to skipping autoreconf.  Distros can change just this one line
# (or provide a command-line override) if they backport any patches that
# touch configure.ac or Makefile.am.
%{!?enable_autotools:%define enable_autotools 0}

# A client only build will create a libvirt.so only containing
# the generic RPC driver, and test driver and no libvirtd
# Default to a full server + client build
%define client_only        0

# Now turn off server build in certain cases

# RHEL-5 builds are client-only for s390, ppc
%if 0%{?rhel} == 5
    %ifnarch %{ix86} x86_64 ia64
        %define client_only        1
    %endif
%endif

# Disable all server side drivers if client only build requested
#%if %{client_only}
#    %define server_drivers     0
#%else
    %define server_drivers     1
#%endif

# Always build with dlopen'd modules
%define with_driver_modules 1

# Now set the defaults for all the important features, independent
# of any particular OS

# First the daemon itself
%define with_libvirtd      0%{!?_without_libvirtd:%{server_drivers}}
%define with_avahi         0%{!?_without_avahi:%{server_drivers}}

# Then the hypervisor drivers that run in libvirtd
%define with_xen           0%{!?_without_xen:%{server_drivers}}
%define with_qemu          0%{!?_without_qemu:%{server_drivers}}
%define with_lxc           0%{!?_without_lxc:%{server_drivers}}
%define with_uml           0%{!?_without_uml:%{server_drivers}}
%define with_libxl         0%{!?_without_libxl:%{server_drivers}}

%define with_qemu_tcg      %{with_qemu}
# Change if we ever provide qemu-kvm binaries on non-x86 hosts
%if 0%{?fedora} >= 18 || 0%{?mcp} >= 8
    %define qemu_kvm_arches    %{ix86} x86_64 ppc64 s390x
%else
    %define qemu_kvm_arches    %{ix86} x86_64
%endif

%ifarch %{qemu_kvm_arches}
    %define with_qemu_kvm      %{with_qemu}
%else
    %define with_qemu_kvm      0
%endif

# Then the hypervisor drivers that run outside libvirtd, in libvirt.so
%define with_openvz        0%{!?_without_openvz:1}
%define with_vbox          0%{!?_without_vbox:1}
%define with_vmware        0%{!?_without_vmware:1}
%define with_phyp          0%{!?_without_phyp:1}
%define with_esx           0%{!?_without_esx:1}
%define with_hyperv        0%{!?_without_hyperv:1}
%define with_xenapi        0%{!?_without_xenapi:1}
%define with_parallels     0%{!?_without_parallels:1}

# Then the secondary host drivers, which run inside libvirtd
%define with_interface        0%{!?_without_interface:%{server_drivers}}
%define with_network          0%{!?_without_network:%{server_drivers}}
%define with_storage_fs       0%{!?_without_storage_fs:%{server_drivers}}
%define with_storage_lvm      0%{!?_without_storage_lvm:%{server_drivers}}
%define with_storage_iscsi    0%{!?_without_storage_iscsi:%{server_drivers}}
%define with_storage_disk     0%{!?_without_storage_disk:%{server_drivers}}
%define with_storage_mpath    0%{!?_without_storage_mpath:%{server_drivers}}
%if 0%{?fedora} >= 16 || 0%{?mcp} >= 8
    %define with_storage_rbd      0%{!?_without_storage_rbd:%{server_drivers}}
%else
    %define with_storage_rbd      0
%endif
%if 0%{?fedora} >= 17 || 0%{?mcp} >= 8
    %define with_storage_sheepdog 0%{!?_without_storage_sheepdog:%{server_drivers}}
%else
    %define with_storage_sheepdog 0
%endif
%define with_numactl          0%{!?_without_numactl:%{server_drivers}}
%define with_selinux          0%{!?_without_selinux:%{server_drivers}}
# Just hardcode to off, since few people ever have apparmor RPMs installed
%define with_apparmor         0%{!?_without_apparmor:0}

# A few optional bits off by default, we enable later
%define with_polkit        0%{!?_without_polkit:0}
%define with_capng         0%{!?_without_capng:0}
%define with_fuse          0%{!?_without_fuse:0}
%define with_netcf         0%{!?_without_netcf:0}
%define with_udev          0%{!?_without_udev:0}
%define with_hal           0%{!?_without_hal:0}
%define with_yajl          0%{!?_without_yajl:0}
%define with_nwfilter      0%{!?_without_nwfilter:0}
%define with_libpcap       0%{!?_without_libpcap:0}
%define with_macvtap       0%{!?_without_macvtap:0}
%define with_libnl         0%{!?_without_libnl:0}
%define with_audit         0%{!?_without_audit:0}
%define with_dtrace        0%{!?_without_dtrace:0}
%define with_cgconfig      0%{!?_without_cgconfig:0}
%define with_sanlock       0%{!?_without_sanlock:0}
%define with_systemd       0%{!?_without_systemd:0}
%define with_numad         0%{!?_without_numad:0}
%define with_firewalld     0%{!?_without_firewalld:0}
%define with_libssh2       0%{!?_without_libssh2:0}

# Non-server/HV driver defaults which are always enabled
%define with_python        0%{!?_without_python:1}
%define with_sasl          0%{!?_without_sasl:1}

# LTC: disable python on cross
%{?cross_build:%define with_python 0}

# Finally set the OS / architecture specific special cases

# Xen is available only on i386 x86_64 ia64
%ifnarch %{ix86} x86_64 ia64
    %define with_xen 0
    %define with_libxl 0
%endif

# Numactl is not available on s390[x] and ARM
%ifarch s390 s390x %{arm}
    %define with_numactl 0
%endif

# RHEL doesn't ship OpenVZ, VBox, UML, PowerHypervisor,
# VMWare, libxenserver (xenapi), libxenlight (Xen 4.1 and newer),
# or HyperV.
%if 0%{?rhel} || 0%{?mcp}
    %define with_openvz 0
    %define with_vbox 0
    %define with_uml 0
    %define with_phyp 0
    %define with_vmware 0
    %define with_xenapi 0
    %define with_libxl 0
    %define with_hyperv 0
    %define with_parallels 0
%endif

# Fedora 17 / RHEL-7 are first where we use systemd. Although earlier
# Fedora has systemd, libvirt still used sysvinit there.
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?mcp} >= 8
    %define with_systemd 1
%endif

# Fedora 18 / RHEL-7 are first where firewalld support is enabled
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?mcp} >= 8
    %define with_firewalld 1
%endif

# RHEL-5 has restricted QEMU to x86_64 only and is too old for LXC
%if 0%{?rhel} == 5
    %define with_qemu_tcg 0
    %ifnarch x86_64
        %define with_qemu 0
        %define with_qemu_kvm 0
    %endif
    %define with_lxc 0
%endif

# RHEL-6 has restricted QEMU to x86_64 only, stopped including Xen
# on all archs. Other archs all have LXC available though
%if 0%{?rhel} >= 6
    %define with_qemu_tcg 0
    %ifnarch x86_64
        %define with_qemu 0
        %define with_qemu_kvm 0
    %endif
    %define with_xen 0
%endif

# Fedora doesn't have any QEMU on ppc64 until FC16 - only ppc
%if (0%{?fedora} && 0%{?fedora} < 16)
    %ifarch ppc64
        %define with_qemu 0
    %endif
%endif

# Fedora doesn't have new enough Xen for libxl until F18
%if (0%{?fedora} && 0%{?fedora} < 18)
    %define with_libxl 0
%endif

# PolicyKit was introduced in Fedora 8 / RHEL-6 or newer
%if 0%{?fedora} >= 8 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
    %define with_polkit    0%{!?_without_polkit:1}
%endif

# libcapng is used to manage capabilities in Fedora 12 / RHEL-6 or newer
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
    %define with_capng     0%{!?_without_capng:1}
%endif

# fuse is used to provide virtualized /proc for LXC
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?mcp} >= 8
    %define with_fuse      0%{!?_without_fuse:1}
%endif

# netcf is used to manage network interfaces in Fedora 12 / RHEL-6 or newer
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
    %define with_netcf     0%{!?_without_netcf:%{server_drivers}}
%endif

# udev is used to manage host devices in Fedora 12 / RHEL-6 or newer
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
    %define with_udev     0%{!?_without_udev:%{server_drivers}}
%else
    %define with_hal       0%{!?_without_hal:%{server_drivers}}
%endif

# interface requires netcf
%if ! 0%{?with_netcf}
    %define with_interface     0
%endif

# Enable yajl library for JSON mode with QEMU
%if 0%{?fedora} >= 13 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
    %define with_yajl     0%{!?_without_yajl:%{server_drivers}}
%endif

# Enable sanlock library for lock management with QEMU
# Sanlock is available only on i686 x86_64 for RHEL
%if 0%{?fedora} >= 16 || 0%{?mcp} >= 8
    %define with_sanlock 0%{!?_without_sanlock:%{server_drivers}}
%endif
%if 0%{?rhel} >= 6 || 0%{?mcp} >= 7
    %ifarch %{ix86} x86_64
        %define with_sanlock 0%{!?_without_sanlock:%{server_drivers}}
    %endif
%endif

# Enable libssh2 transport for new enough distros
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
    %define with_libssh2 0%{!?_without_libssh2:1}
%endif

# Disable some drivers when building without libvirt daemon.
# The logic is the same as in configure.ac
%if ! %{with_libvirtd}
    %define with_interface 0
    %define with_network 0
    %define with_qemu 0
    %define with_lxc 0
    %define with_uml 0
    %define with_hal 0
    %define with_udev 0
    %define with_storage_fs 0
    %define with_storage_lvm 0
    %define with_storage_iscsi 0
    %define with_storage_mpath 0
    %define with_storage_rbd 0
    %define with_storage_sheepdog 0
    %define with_storage_disk 0
%endif

%if %{with_qemu} || %{with_lxc} || %{with_uml}
    %define with_nwfilter 0%{!?_without_nwfilter:%{server_drivers}}
# Enable libpcap library
    %define with_libpcap  0%{!?_without_libpcap:%{server_drivers}}
    %define with_macvtap  0%{!?_without_macvtap:%{server_drivers}}

# numad is used to manage the CPU and memory placement dynamically,
# it's not available on s390[x] and ARM.
    %if 0%{?fedora} >= 17 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
        %ifnarch s390 s390x %{arm}
            %define with_numad    0%{!?_without_numad:%{server_drivers}}
        %endif
    %endif
%endif

%if %{with_macvtap}
    %define with_libnl 1
%endif

%if 0%{?fedora} >= 11 || 0%{?rhel} >= 5 || 0%{?mcp} >= 6
    %define with_audit    0%{!?_without_audit:1}
%endif

%if 0%{?fedora} >= 13 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
    %define with_dtrace 1
%endif

# Pull in cgroups config system
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
    %if %{with_qemu} || %{with_lxc}
        %define with_cgconfig 0%{!?_without_cgconfig:1}
    %endif
%endif

%if %{with_udev} || %{with_hal}
    %define with_nodedev 1
%else
    %define with_nodedev 0
%endif

%if %{with_storage_fs} || %{with_storage_mpath} || %{with_storage_iscsi} || %{with_storage_lvm} || %{with_storage_disk}
    %define with_storage 1
%else
    %define with_storage 0
%endif


# Force QEMU to run as non-root
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
    %define qemu_user  qemu
    %define qemu_group  qemu
%else
    %define qemu_user  root
    %define qemu_group  root
%endif


# The RHEL-5 Xen package has some feature backports. This
# flag is set to enable use of those special bits on RHEL-5
%if 0%{?rhel} == 5
    %define with_rhel5  1
%else
    %define with_rhel5  0
%endif

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7 || 0%{?mcp} >= 8
    %define with_systemd_macros 1
%else
    %define with_systemd_macros 0
%endif


Summary: Library providing a simple virtualization API
Name: libvirt
Version: 1.1.3
%define release .1
%define frobisher_release .5
Release: 1%{?dist}%{frobisher_release}%{?release}%{?extra_release}
# MCP: exclude cross arches for this package
ExcludeArch: %{cross_arches}
License: LGPLv2+
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
URL: http://libvirt.org/

%if %(echo %{version} | grep -o \\. | wc -l) == 3
    %define mainturl stable_updates/
%endif

Requires(pre): qemu

BuildRequires: git

%if %{with_libvirtd}
Requires: libvirt-daemon = %{version}-%{release}
    %if %{with_network}
Requires: libvirt-daemon-config-network = %{version}-%{release}
    %endif
    %if %{with_nwfilter}
Requires: libvirt-daemon-config-nwfilter = %{version}-%{release}
    %endif
    %if %{with_driver_modules}
        %if %{with_libxl}
Requires: libvirt-daemon-driver-libxl = %{version}-%{release}
        %endif
        %if %{with_lxc}
Requires: libvirt-daemon-driver-lxc = %{version}-%{release}
        %endif
        %if %{with_qemu}
Requires: libvirt-daemon-driver-qemu = %{version}-%{release}
        %endif
        %if %{with_uml}
Requires: libvirt-daemon-driver-uml = %{version}-%{release}
        %endif
        %if %{with_xen}
Requires: libvirt-daemon-driver-xen = %{version}-%{release}
        %endif

Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
    %endif
%endif
Requires: libvirt-client = %{version}-%{release}

# All build-time requirements. Run-time requirements are
# listed against each sub-RPM
#%if 0%{?enable_autotools}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: libtool
BuildRequires: /usr/bin/pod2man
#%endif
%if %{with_python}
BuildRequires: python-devel
%endif
%if %{with_systemd}
BuildRequires: systemd-units
BuildRequires: libcgroup
%endif
%if %{with_xen}
BuildRequires: xen-devel
%endif
BuildRequires: libxml2-devel
BuildRequires: xhtml1-dtds
BuildRequires: libxslt
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gettext
BuildRequires: libtasn1-devel
BuildRequires: gnutls-devel
BuildRequires: libattr-devel
%if %{with_libvirtd}
# For pool-build probing for existing pools
BuildRequires: libblkid-devel >= 2.17
%endif
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
# for augparse, optionally used in testing
BuildRequires: augeas
%endif
%if %{with_hal}
BuildRequires: hal-devel
%endif
%if %{with_udev}
    %if 0%{?fedora} >= 18 || 0%{?rhel} >= 7 || 0%{?mcp} >= 8
BuildRequires: systemd-devel >= 185
    %else
BuildRequires: libudev-devel >= 145
    %endif
BuildRequires: libpciaccess-devel >= 0.10.9
%endif
%if %{with_yajl}
BuildRequires: yajl-devel
%endif
%if %{with_sanlock}
# make sure libvirt is built with new enough sanlock on
# distros that have it; required for on_lockfailure
    %if 0%{?fedora} >= 17 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
BuildRequires: sanlock-devel >= 2.4
    %else
BuildRequires: sanlock-devel >= 1.8
    %endif
%endif
%if %{with_libpcap}
BuildRequires: libpcap-devel
%endif
%if %{with_libnl}
    %if 0%{?fedora} >= 18 || 0%{?rhel} >= 7 || 0%{?mcp} >= 8
BuildRequires: libnl3-devel
    %else
BuildRequires: libnl-devel
    %endif
%endif
%if %{with_avahi}
BuildRequires: avahi-devel
%endif
%if %{with_selinux}
BuildRequires: libselinux-devel
%endif
%if %{with_apparmor}
BuildRequires: libapparmor-devel
%endif
%if %{with_network}
BuildRequires: dnsmasq >= 2.41
BuildRequires: iptables
BuildRequires: iptables-ipv6
BuildRequires: radvd
%endif
%if %{with_nwfilter}
BuildRequires: ebtables
%endif
BuildRequires: module-init-tools
%if %{with_sasl}
BuildRequires: cyrus-sasl-devel
%endif
%if %{with_polkit}
    %if 0%{?fedora} >= 12 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
# Only need the binary, not -devel
BuildRequires: polkit >= 0.93
    %else
BuildRequires: PolicyKit-devel >= 0.6
    %endif
%endif
%if %{with_storage_fs}
# For mount/umount in FS driver
BuildRequires: util-linux
%endif
%if %{with_qemu}
# From QEMU RPMs
BuildRequires: /usr/bin/qemu-img
%else
    %if %{with_xen}
# From Xen RPMs
BuildRequires: /usr/sbin/qcow-create
    %endif
%endif
%if %{with_storage_lvm}
# For LVM drivers
BuildRequires: lvm2
%endif
%if %{with_storage_iscsi}
# For ISCSI driver
BuildRequires: iscsi-initiator-utils
%endif
%if %{with_storage_disk}
# For disk driver
BuildRequires: parted-devel
    %if 0%{?rhel} == 5
# Broken RHEL-5 parted RPM is missing a dep
BuildRequires: e2fsprogs-devel
    %endif
%endif
%if %{with_storage_mpath}
# For Multipath support
    %if 0%{?rhel} == 5
# Broken RHEL-5 packaging has header files in main RPM :-(
BuildRequires: device-mapper
    %else
BuildRequires: device-mapper-devel
    %endif
    %if %{with_storage_rbd}
BuildRequires: ceph-devel
    %endif
%endif
%if %{with_numactl}
# For QEMU/LXC numa info
BuildRequires: numactl-devel
%endif
%if %{with_capng}
BuildRequires: libcap-ng-devel >= 0.5.0
%endif
%if %{with_fuse}
BuildRequires: fuse-devel >= 2.8.6
%endif
%if %{with_phyp} || %{with_libssh2}
BuildRequires: libssh2-devel >= 1.3.0
%endif

%if %{with_netcf}
    %if 0%{?fedora} >= 18 || 0%{?rhel} >= 7 || 0%{?mcp} >= 8
BuildRequires: netcf-devel >= 0.2.2
    %else
        %if 0%{?fedora} >= 16 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
BuildRequires: netcf-devel >= 0.1.8
        %else
BuildRequires: netcf-devel >= 0.1.4
        %endif
    %endif
%endif
%if %{with_esx}
    %if 0%{?fedora} >= 9 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
BuildRequires: libcurl-devel
    %else
BuildRequires: curl-devel
    %endif
%endif
%if %{with_hyperv}
BuildRequires: libwsman-devel >= 2.2.3
%endif
%if %{with_audit}
BuildRequires: audit-libs-devel
%endif
%if %{with_dtrace}
# we need /usr/sbin/dtrace
BuildRequires: systemtap-sdt-devel
%endif

%if %{with_storage_fs}
# For mount/umount in FS driver
BuildRequires: util-linux
# For showmount in FS driver (netfs discovery)
BuildRequires: nfs-utils
%endif

%if %{with_firewalld}
# Communication with the firewall daemon uses DBus
BuildRequires: dbus-devel
%endif

# Fedora build root suckage
BuildRequires: gawk

# For storage wiping with different algorithms
BuildRequires: scrub

%if %{with_numad}
BuildRequires: numad
%endif

Provides: bundled(gnulib)

%description
Libvirt is a C toolkit to interact with the virtualization capabilities
of recent versions of Linux (and other OSes). The main package includes
the libvirtd server exporting the virtualization support.

%package docs
Summary: API reference and website documentation
Group: Development/Libraries

%description docs
Includes the API reference for the libvirt C library, and a complete
copy of the libvirt.org website documentation.

%if %{with_libvirtd}
%package daemon
Summary: Server side daemon and supporting files for libvirt library
Group: Development/Libraries

# All runtime requirements for the libvirt package (runtime requrements
# for subpackages are listed later in those subpackages)

# The client side, i.e. shared libs and virsh are in a subpackage
Requires: %{name}-client = %{version}-%{release}

# for modprobe of pci devices
Requires: module-init-tools
# for /sbin/ip & /sbin/tc
Requires: iproute
    %if %{with_avahi}
        %if 0%{?rhel} == 5
Requires: avahi
        %else
Requires: avahi-libs
        %endif
    %endif
    %if %{with_network}
Requires: dnsmasq >= 2.41
Requires: radvd
    %endif
    %if %{with_network} || %{with_nwfilter}
Requires: iptables
Requires: iptables-ipv6
    %endif
    %if %{with_nwfilter}
Requires: ebtables
    %endif
    %if %{with_netcf} && (0%{?fedora} >= 18 || 0%{?rhel} >= 7 || 0%{?rhel} >= 8 || 0%{?mcp} >= 8)
Requires: netcf-libs >= 0.2.2
    %endif
# needed for device enumeration
    %if %{with_hal}
Requires: hal
    %endif
    %if %{with_udev}
        %if 0%{?fedora} >= 18 || 0%{?rhel} >= 7 || 0%{?mcp} >= 8
Requires: systemd >= 185
        %else
Requires: udev >= 145
        %endif
    %endif
    %if %{with_polkit}
        %if 0%{?fedora} >= 12 || 0%{?rhel} >=6 || 0%{?mcp} >= 7
Requires: polkit >= 0.93
        %else
Requires: PolicyKit >= 0.6
        %endif
    %endif
    %if %{with_storage_fs}
Requires: nfs-utils
# For mkfs
Requires: util-linux
# For glusterfs
        %if 0%{?fedora} >= 11 || 0%{?mcp} >= 8
Requires: glusterfs-client >= 2.0.1
        %endif
    %endif
    %if %{with_qemu}
# From QEMU RPMs
Requires: /usr/bin/qemu-img
# For image compression
Requires: gzip
Requires: bzip2
Requires: lzop
Requires: xz
    %else
        %if %{with_xen}
# From Xen RPMs
Requires: /usr/sbin/qcow-create
        %endif
    %endif
    %if %{with_storage_lvm}
# For LVM drivers
Requires: lvm2
    %endif
    %if %{with_storage_iscsi}
# For ISCSI driver
Requires: iscsi-initiator-utils
    %endif
    %if %{with_storage_disk}
# For disk driver
Requires: parted
Requires: device-mapper
    %endif
    %if %{with_storage_mpath}
# For multipath support
Requires: device-mapper
    %endif
    %if %{with_storage_sheepdog}
# For Sheepdog support
Requires: sheepdog
    %endif
    %if %{with_cgconfig}
Requires: libcgroup
    %endif
    %ifarch %{ix86} x86_64 ia64
# For virConnectGetSysinfo
Requires: dmidecode
    %endif
# For service management
    %if %{with_systemd}
Requires(post): systemd-units
Requires(post): systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units
    %endif
    %if %{with_numad}
Requires: numad
    %endif
# libvirtd depends on 'messagebus' service
Requires: dbus
# For uid creation during pre
Requires(pre): shadow-utils

%description daemon
Server side daemon required to manage the virtualization capabilities
of recent versions of Linux. Requires a hypervisor specific sub-RPM
for specific drivers.

    %if %{with_network}
%package daemon-config-network
Summary: Default configuration files for the libvirtd daemon
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}

%description daemon-config-network
Default configuration files for setting up NAT based networking
    %endif

    %if %{with_nwfilter}
%package daemon-config-nwfilter
Summary: Network filter configuration files for the libvirtd daemon
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}

%description daemon-config-nwfilter
Network filter configuration files for cleaning guest traffic
    %endif

    %if %{with_driver_modules}
        %if %{with_network}
%package daemon-driver-network
Summary: Network driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-network
The network driver plugin for the libvirtd daemon, providing
an implementation of the virtual network APIs using the Linux
bridge capabilities.
        %endif


        %if %{with_nwfilter}
%package daemon-driver-nwfilter
Summary: Nwfilter driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-nwfilter
The nwfilter driver plugin for the libvirtd daemon, providing
an implementation of the firewall APIs using the ebtables,
iptables and ip6tables capabilities
        %endif


        %if %{with_nodedev}
%package daemon-driver-nodedev
Summary: Nodedev driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-nodedev
The nodedev driver plugin for the libvirtd daemon, providing
an implementation of the node device APIs using the udev
capabilities.
        %endif


        %if %{with_interface}
%package daemon-driver-interface
Summary: Interface driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-interface
The interface driver plugin for the libvirtd daemon, providing
an implementation of the network interface APIs using the
netcf library
        %endif


%package daemon-driver-secret
Summary: Secret driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-secret
The secret driver plugin for the libvirtd daemon, providing
an implementation of the secret key APIs.


        %if %{with_storage}
%package daemon-driver-storage
Summary: Storage driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-storage
The storage driver plugin for the libvirtd daemon, providing
an implementation of the storage APIs using LVM, iSCSI,
parted and more.
        %endif


        %if %{with_qemu}
%package daemon-driver-qemu
Summary: Qemu driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}
# There really is a hard cross-driver dependency here
Requires: libvirt-daemon-driver-network = %{version}-%{release}

%description daemon-driver-qemu
The qemu driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
QEMU
        %endif


        %if %{with_lxc}
%package daemon-driver-lxc
Summary: LXC driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}
# There really is a hard cross-driver dependency here
Requires: libvirt-daemon-driver-network = %{version}-%{release}

%description daemon-driver-lxc
The LXC driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
the Linux kernel
        %endif


        %if %{with_uml}
%package daemon-driver-uml
Summary: Uml driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-uml
The UML driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
User Mode Linux
        %endif


        %if %{with_xen}
%package daemon-driver-xen
Summary: Xen driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-xen
The Xen driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
Xen
        %endif


        %if %{with_libxl}
%package daemon-driver-libxl
Summary: Libxl driver plugin for the libvirtd daemon
Group: Development/Libraries
Requires: libvirt-daemon = %{version}-%{release}

%description daemon-driver-libxl
The Libxl driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
Libxl
        %endif
    %endif # %{with_driver_modules}



    %if %{with_qemu_tcg}
%package daemon-qemu
Summary: Server side daemon & driver required to run QEMU guests
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
Requires: libvirt-daemon-driver-qemu = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
        %endif
Requires: qemu

%description daemon-qemu
Server side daemon and driver required to manage the virtualization
capabilities of the QEMU TCG emulators
    %endif


    %if %{with_qemu_kvm}
%package daemon-kvm
Summary: Server side daemon & driver required to run KVM guests
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
Requires: libvirt-daemon-driver-qemu = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
        %endif
Requires: qemu-kvm

%description daemon-kvm
Server side daemon and driver required to manage the virtualization
capabilities of the KVM hypervisor
    %endif


    %if %{with_lxc}
%package daemon-lxc
Summary: Server side daemon & driver required to run LXC guests
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
Requires: libvirt-daemon-driver-lxc = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
        %endif

%description daemon-lxc
Server side daemon and driver required to manage the virtualization
capabilities of LXC
    %endif


    %if %{with_uml}
%package daemon-uml
Summary: Server side daemon & driver required to run UML guests
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
Requires: libvirt-daemon-driver-uml = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
        %endif
# There are no UML kernel RPMs in Fedora/RHEL to depend on.

%description daemon-uml
Server side daemon and driver required to manage the virtualization
capabilities of UML
    %endif


    %if %{with_xen} || %{with_libxl}
%package daemon-xen
Summary: Server side daemon & driver required to run XEN guests
Group: Development/Libraries

Requires: libvirt-daemon = %{version}-%{release}
        %if %{with_driver_modules}
            %if %{with_xen}
Requires: libvirt-daemon-driver-xen = %{version}-%{release}
            %endif
            %if %{with_libxl}
Requires: libvirt-daemon-driver-libxl = %{version}-%{release}
            %endif
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
        %endif
Requires: xen

%description daemon-xen
Server side daemon and driver required to manage the virtualization
capabilities of XEN
    %endif
%endif # %{with_libvirtd}

%package client
Summary: Client side library and utilities of the libvirt library
Group: Development/Libraries
Requires: readline
Requires: ncurses
# So remote clients can access libvirt over SSH tunnel
# (client invokes 'nc' against the UNIX socket on the server)
Requires: nc
# Needed by libvirt-guests init script.
Requires: gettext
# Needed by virt-pki-validate script.
Requires: gnutls-utils
# Needed for probing the power management features of the host.
Requires: pm-utils
%if %{with_sasl}
Requires: cyrus-sasl
# Not technically required, but makes 'out-of-box' config
# work correctly & doesn't have onerous dependencies
Requires: cyrus-sasl-md5
%endif

%description client
Shared libraries and client binaries needed to access to the
virtualization capabilities of recent versions of Linux (and other OSes).

%package devel
Summary: Libraries, includes, etc. to compile with the libvirt library
Group: Development/Libraries
Requires: %{name}-client = %{version}-%{release}
Requires: %{name}-docs = %{version}-%{release}
Requires: pkgconfig

%description devel
Include header files & development libraries for the libvirt C library.

%if %{with_sanlock}
%package lock-sanlock
Summary: Sanlock lock manager plugin for QEMU driver
Group: Development/Libraries
    %if 0%{?fedora} >= 17 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
Requires: sanlock >= 2.4
    %else
Requires: sanlock >= 1.8
    %endif
#for virt-sanlock-cleanup require augeas
Requires: augeas
Requires: %{name}-daemon = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}

%description lock-sanlock
Includes the Sanlock lock manager plugin for the QEMU
driver
%endif

%if %{with_python}
%package python
Summary: Python bindings for the libvirt library
Group: Development/Libraries
Requires: %{name}-client = %{version}-%{release}

%description python
The libvirt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).
%endif

%debug_package

%prep

git clone --branch powerkvm git://9.3.189.26/frobisher/libvirt.git ./
git log --pretty=oneline | head -n1
git log > ChangeLog
git submodule init
git submodule update

%build
%if ! %{with_xen}
    %define _without_xen --without-xen
%endif

%if ! %{with_qemu}
    %define _without_qemu --without-qemu
%endif

%if ! %{with_openvz}
    %define _without_openvz --without-openvz
%endif

%if ! %{with_lxc}
    %define _without_lxc --without-lxc
%endif

%if ! %{with_vbox}
    %define _without_vbox --without-vbox
%endif

%if ! %{with_xenapi}
    %define _without_xenapi --without-xenapi
%endif

%if ! %{with_libxl}
    %define _without_libxl --without-libxl
%endif

%if ! %{with_sasl}
    %define _without_sasl --without-sasl
%endif

%if ! %{with_avahi}
    %define _without_avahi --without-avahi
%endif

%if ! %{with_phyp}
    %define _without_phyp --without-phyp
%endif

%if ! %{with_esx}
    %define _without_esx --without-esx
%endif

%if ! %{with_hyperv}
    %define _without_hyperv --without-hyperv
%endif

%if ! %{with_vmware}
    %define _without_vmware --without-vmware
%endif

%if ! %{with_parallels}
    %define _without_parallels --without-parallels
%endif

%if ! %{with_polkit}
    %define _without_polkit --without-polkit
%endif

%if ! %{with_python}
    %define _without_python --without-python
%endif

%if ! %{with_libvirtd}
    %define _without_libvirtd --without-libvirtd
%endif

%if ! %{with_uml}
    %define _without_uml --without-uml
%endif

%if %{with_rhel5}
    %define _with_rhel5_api --with-rhel5-api
%endif

%if ! %{with_interface}
    %define _without_interface --without-interface
%endif

%if ! %{with_network}
    %define _without_network --without-network
%endif

%if ! %{with_storage_fs}
    %define _without_storage_fs --without-storage-fs
%endif

%if ! %{with_storage_lvm}
    %define _without_storage_lvm --without-storage-lvm
%endif

%if ! %{with_storage_iscsi}
    %define _without_storage_iscsi --without-storage-iscsi
%endif

%if ! %{with_storage_disk}
    %define _without_storage_disk --without-storage-disk
%endif

%if ! %{with_storage_mpath}
    %define _without_storage_mpath --without-storage-mpath
%endif

%if ! %{with_storage_rbd}
    %define _without_storage_rbd --without-storage-rbd
%endif

%if ! %{with_storage_sheepdog}
    %define _without_storage_sheepdog --without-storage-sheepdog
%endif

%if ! %{with_numactl}
    %define _without_numactl --without-numactl
%endif

%if ! %{with_numad}
    %define _without_numad --without-numad
%endif

%if ! %{with_capng}
    %define _without_capng --without-capng
%endif

%if ! %{with_fuse}
    %define _without_fuse --without-fuse
%endif

%if ! %{with_netcf}
    %define _without_netcf --without-netcf
%endif

%if ! %{with_selinux}
    %define _without_selinux --without-selinux
%endif

%if ! %{with_hal}
    %define _without_hal --without-hal
%endif

%if ! %{with_udev}
    %define _without_udev --without-udev
%endif

%if ! %{with_yajl}
    %define _without_yajl --without-yajl
%endif

%if ! %{with_sanlock}
    %define _without_sanlock --without-sanlock
%endif

%if ! %{with_libpcap}
    %define _without_libpcap --without-libpcap
%endif

%if ! %{with_macvtap}
    %define _without_macvtap --without-macvtap
%endif

%if ! %{with_audit}
    %define _without_audit --without-audit
%endif

%if ! %{with_dtrace}
    %define _without_dtrace --without-dtrace
%endif

%if ! %{with_driver_modules}
    %define _without_driver_modules --without-driver-modules
%endif

%if %{with_firewalld}
    %define _with_firewalld --with-firewalld
%endif

%define when  %(date +"%%F-%%T")
%define where %(hostname)
%define who   %{?packager}%{!?packager:Unknown}
%define with_packager --with-packager="%{who}, %{when}, %{where}"
%define with_packager_version --with-packager-version="%{release}"

%if %{with_systemd}
    %define init_scripts --with-init_script=systemd
%else
    %define init_scripts --with-init_script=redhat
%endif

%if %{with_selinux}
    %if 0%{?fedora} >= 17 || 0%{?rhel} >= 7 || 0%{?mcp} >= 8
        %define with_selinux_mount --with-selinux-mount="/sys/fs/selinux"
    %else
        %define with_selinux_mount --with-selinux-mount="/selinux"
    %endif
%endif

# place macros above and build commands below this comment

%if 0%{?enable_autotools}
 autoreconf -if
%endif

./autogen.sh --system \
           %{?_without_xen} \
           %{?_without_qemu} \
           %{?_without_openvz} \
           %{?_without_lxc} \
           %{?_without_vbox} \
           %{?_without_libxl} \
           %{?_without_xenapi} \
           %{?_without_sasl} \
           %{?_without_avahi} \
           %{?_without_polkit} \
           %{?_without_python} \
           %{?_without_libvirtd} \
           %{?_without_uml} \
           %{?_without_phyp} \
           %{?_without_esx} \
           %{?_without_hyperv} \
           %{?_without_vmware} \
           %{?_without_parallels} \
           %{?_without_interface} \
           %{?_without_network} \
           %{?_with_rhel5_api} \
           %{?_without_storage_fs} \
           %{?_without_storage_lvm} \
           %{?_without_storage_iscsi} \
           %{?_without_storage_disk} \
           %{?_without_storage_mpath} \
           %{?_without_storage_rbd} \
           %{?_without_storage_sheepdog} \
           %{?_without_numactl} \
           %{?_without_numad} \
           %{?_without_capng} \
           %{?_without_fuse} \
           %{?_without_netcf} \
           %{?_without_selinux} \
           %{?_with_selinux_mount} \
           %{?_without_apparmor} \
           %{?_without_hal} \
           %{?_without_udev} \
           %{?_without_yajl} \
           %{?_without_sanlock} \
           %{?_without_libpcap} \
           %{?_without_macvtap} \
           %{?_without_audit} \
           %{?_without_dtrace} \
           %{?_without_driver_modules} \
           %{?_with_firewalld} \
           %{with_packager} \
           %{with_packager_version} \
           --with-qemu-user=%{qemu_user} \
           --with-qemu-group=%{qemu_group} \
           %{init_scripts}
make %{?_smp_mflags}
gzip -9 ChangeLog

%install
rm -fr %{buildroot}

# Avoid using makeinstall macro as it changes prefixes rather than setting
# DESTDIR. Newer make_install macro would be better but it's not available
# on RHEL 5, thus we need to expand it here.
make install DESTDIR=%{?buildroot} SYSTEMD_UNIT_DIR=%{_unitdir}

for i in domain-events/events-c dominfo domsuspend hellolibvirt openauth python xml/nwfilter systemtap
do
  (cd examples/$i ; make clean ; rm -rf .deps .libs Makefile Makefile.in)
done
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt/lock-driver/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt/lock-driver/*.a
%if %{with_driver_modules}
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt/connection-driver/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt/connection-driver/*.a
%endif

%if %{with_network}
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/lib/libvirt/dnsmasq/
# We don't want to install /etc/libvirt/qemu/networks in the main %files list
# because if the admin wants to delete the default network completely, we don't
# want to end up re-incarnating it on every RPM upgrade.
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/libvirt/networks/
cp $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/default.xml \
   $RPM_BUILD_ROOT%{_datadir}/libvirt/networks/default.xml
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/default.xml
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
# Strip auto-generated UUID - we need it generated per-install
sed -i -e "/<uuid>/d" $RPM_BUILD_ROOT%{_datadir}/libvirt/networks/default.xml
%else
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/default.xml
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
%endif
%if ! %{with_qemu}
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirtd_qemu.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
%endif
%find_lang %{name}

%if ! %{with_sanlock}
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirt_sanlock.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirt_sanlock.aug
%endif

%if ! %{with_lxc}
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirtd_lxc.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirtd_lxc.aug
%endif

%if ! %{with_python}
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libvirt-python-%{version}
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libvirt-python-%{version}/examples
%endif

%if ! %{with_qemu}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu.conf
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/libvirtd.qemu
%endif
%if ! %{with_lxc}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/lxc.conf
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/libvirtd.lxc
%endif
%if ! %{with_uml}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/libvirtd.uml
%endif

mv $RPM_BUILD_ROOT%{_datadir}/doc/libvirt-%{version} \
   $RPM_BUILD_ROOT%{_datadir}/doc/libvirt-docs-%{version}

%if %{with_dtrace}
    %ifarch %{power64} s390x x86_64 ia64 alpha sparc64
mv $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_probes.stp \
   $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_probes-64.stp
mv $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_qemu_probes.stp \
   $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_qemu_probes-64.stp
    %endif
%endif

%if 0%{?fedora} < 14 && 0%{?rhel} < 6 && 0%{?mcp} < 7
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/sysctl.d/libvirtd.conf
%endif

%clean
rm -fr %{buildroot}

%check
cd tests
make
# These tests don't current work in a mock build root
for i in nodeinfotest seclabeltest
do
  rm -f $i
  printf 'int main(void) { return 0; }' > $i.c
  printf '#!/bin/sh\nexit 0\n' > $i
  chmod +x $i
done
make check

%if %{with_libvirtd}
%pre daemon
    %if 0%{?fedora} >= 12 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
# We want soft static allocation of well-known ids, as disk images
# are commonly shared across NFS mounts by id rather than name; see
# https://fedoraproject.org/wiki/Packaging:UsersAndGroups
getent group kvm >/dev/null || groupadd -f -g 36 -r kvm
getent group qemu >/dev/null || groupadd -f -g 107 -r qemu
if ! getent passwd qemu >/dev/null; then
  if ! getent passwd 107 >/dev/null; then
    useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin -c "qemu user" qemu
  else
    useradd -r -g qemu -G kvm -d / -s /sbin/nologin -c "qemu user" qemu
  fi
fi
exit 0
    %endif

%post daemon

    %if %{with_network}
# All newly defined networks will have a mac address for the bridge
# auto-generated, but networks already existing at the time of upgrade
# will not. We need to go through all the network configs, look for
# those that don't have a mac address, and add one.

network_files=$( (cd %{_localstatedir}/lib/libvirt/network && \
                  grep -L "mac address" *.xml; \
                  cd %{_sysconfdir}/libvirt/qemu/networks && \
                  grep -L "mac address" *.xml) 2>/dev/null \
                | sort -u)

for file in $network_files
do
   # each file exists in either the config or state directory (or both) and
   # does not have a mac address specified in either. We add the same mac
   # address to both files (or just one, if the other isn't there)

   mac4=`printf '%X' $(($RANDOM % 256))`
   mac5=`printf '%X' $(($RANDOM % 256))`
   mac6=`printf '%X' $(($RANDOM % 256))`
   for dir in %{_localstatedir}/lib/libvirt/network \
              %{_sysconfdir}/libvirt/qemu/networks
   do
      if test -f $dir/$file
      then
         sed -i.orig -e \
           "s|\(<bridge.*$\)|\0\n  <mac address='52:54:00:$mac4:$mac5:$mac6'/>|" \
           $dir/$file
         if test $? != 0
         then
             echo "failed to add <mac address='52:54:00:$mac4:$mac5:$mac6'/>" \
                  "to $dir/$file"
             mv -f $dir/$file.orig $dir/$file
         else
             rm -f $dir/$file.orig
         fi
      fi
   done
done
    %endif

    %if %{with_systemd}
        %if %{with_systemd_macros}
            %systemd_post libvirtd.service
        %else
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl enable virtlockd.socket >/dev/null 2>&1 || :
    /bin/systemctl enable libvirtd.service >/dev/null 2>&1 || :
fi
        %endif
    %else
        %if %{with_cgconfig}
# Starting with Fedora 16/RHEL-7, systemd automounts all cgroups,
# and cgconfig is no longer a necessary service.
            %if (0%{?rhel} && 0%{?rhel} < 7) || (0%{?fedora} && 0%{?fedora} < 16) || (0%{?mcp} && 0%{?mcp} < 8)
if [ "$1" -eq "1" ]; then
/sbin/chkconfig cgconfig on
fi
            %endif
        %endif

/sbin/chkconfig --add libvirtd
if [ "$1" -ge "1" ]; then
    /sbin/service libvirtd condrestart > /dev/null 2>&1
fi
    %endif

%preun daemon
    %if %{with_systemd}
        %if %{with_systemd_macros}
            %systemd_preun libvirtd.service
        %else
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable virtlockd.socket > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable libvirtd.service > /dev/null 2>&1 || :
    /bin/systemctl stop libvirtd.service > /dev/null 2>&1 || :
    /bin/systemctl stop virtlockd.service > /dev/null 2>&1 || :
fi
        %endif
    %else
if [ $1 = 0 ]; then
    /sbin/service libvirtd stop 1>/dev/null 2>&1
    /sbin/chkconfig --del libvirtd
fi
    %endif

%postun daemon
    %if %{with_systemd}
        %if %{with_systemd_macros}
            %systemd_postun_with_restart libvirtd.service
        %else
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl status virtlockd.service >/dev/null 2>&1
    if [ $? = 1 ] ; then
        /bin/systemctl kill --signal=USR1 virtlockd.service >/dev/null 2>&1 || :
    fi
    /bin/systemctl try-restart libvirtd.service >/dev/null 2>&1 || :
fi
        %endif
    %endif

    %if %{with_network}
%post daemon-config-network
if test $1 -eq 1 && test ! -f %{_sysconfdir}/libvirt/qemu/networks/default.xml ; then
    UUID=`/usr/bin/uuidgen`
    sed -e "s,</name>,</name>\n  <uuid>$UUID</uuid>," \
         < %{_datadir}/libvirt/networks/default.xml \
         > %{_sysconfdir}/libvirt/qemu/networks/default.xml
    ln -s ../default.xml %{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
fi
    %endif

    %if %{with_systemd}
%triggerun -- libvirt < 0.9.4
%{_bindir}/systemd-sysv-convert --save libvirtd >/dev/null 2>&1 ||:

# If the package is allowed to autostart:
/bin/systemctl --no-reload enable libvirtd.service >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del libvirtd >/dev/null 2>&1 || :
/bin/systemctl try-restart libvirtd.service >/dev/null 2>&1 || :
    %endif
%endif # %{with_libvirtd}

%preun client

%if %{with_systemd}
    %if %{with_systemd_macros}
        %systemd_preun libvirt-guests.service
    %endif
%else
if [ $1 = 0 ]; then
    /sbin/chkconfig --del libvirt-guests
    rm -f /var/lib/libvirt/libvirt-guests
fi
%endif

%post client

/sbin/ldconfig
%if %{with_systemd}
    %if %{with_systemd_macros}
        %systemd_post libvirt-guests.service
    %endif
%else
/sbin/chkconfig --add libvirt-guests
%endif

%postun client

/sbin/ldconfig
%if %{with_systemd}
    %if %{with_systemd_macros}
        %systemd_postun_with_restart libvirt-guests.service
    %endif
%triggerun client -- libvirt < 0.9.4
%{_bindir}/systemd-sysv-convert --save libvirt-guests >/dev/null 2>&1 ||:

# If the package is allowed to autostart:
/bin/systemctl --no-reload enable libvirt-guests.service >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del libvirt-guests >/dev/null 2>&1 || :
/bin/systemctl try-restart libvirt-guests.service >/dev/null 2>&1 || :
%endif

%if %{with_sanlock}
%post lock-sanlock
if getent group sanlock > /dev/null ; then
    chmod 0770 %{_localstatedir}/lib/libvirt/sanlock
    chown root:sanlock %{_localstatedir}/lib/libvirt/sanlock
fi
%endif

%files
%defattr(-, root, root)

%files docs
%defattr(-, root, root)
# Website
%dir %{_datadir}/doc/libvirt-docs-%{version}
%dir %{_datadir}/doc/libvirt-docs-%{version}/html
%{_datadir}/doc/libvirt-docs-%{version}/html/*

# API docs
%dir %{_datadir}/gtk-doc/html/libvirt/
%doc %{_datadir}/gtk-doc/html/libvirt/*.devhelp
%doc %{_datadir}/gtk-doc/html/libvirt/*.html
%doc %{_datadir}/gtk-doc/html/libvirt/*.png
%doc %{_datadir}/gtk-doc/html/libvirt/*.css

%if %{with_libvirtd}
%files daemon
%defattr(-, root, root)

# remove COPYING.LIB
%doc AUTHORS ChangeLog.gz README TODO COPYING.LESSER
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/

    %if %{with_network}
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/autostart
    %endif

%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/nwfilter/

    %if %{with_systemd}
%{_unitdir}/libvirtd.service
%{_unitdir}/virtlockd.service
%{_unitdir}/virtlockd.socket
    %else
%{_sysconfdir}/rc.d/init.d/libvirtd
%{_sysconfdir}/rc.d/init.d/virtlockd
    %endif
%doc daemon/libvirtd.upstart
%config(noreplace) %{_sysconfdir}/sysconfig/libvirtd
%config(noreplace) %{_sysconfdir}/sysconfig/virtlockd
%config(noreplace) %{_sysconfdir}/libvirt/libvirtd.conf
%config(noreplace) %{_sysconfdir}/libvirt/virtlockd.conf

    %if 0%{?fedora} >= 14 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
%config(noreplace) %{_prefix}/lib/sysctl.d/libvirtd.conf
    %endif
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/lxc/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/uml/
    %if %{with_libxl}
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/libxl/
    %endif

%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd
    %if %{with_qemu}
%config(noreplace) %{_sysconfdir}/libvirt/qemu.conf
%config(noreplace) %{_sysconfdir}/libvirt/qemu-lockd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.qemu
    %endif
    %if %{with_lxc}
%config(noreplace) %{_sysconfdir}/libvirt/lxc.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.lxc
    %endif
    %if %{with_uml}
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.uml
    %endif

%dir %{_datadir}/libvirt/

    %if %{with_network}
%dir %{_datadir}/libvirt/networks/
%{_datadir}/libvirt/networks/default.xml
    %endif

%ghost %dir %{_localstatedir}/run/libvirt/

%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/images/
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/filesystems/
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/boot/
%dir %attr(0711, root, root) %{_localstatedir}/cache/libvirt/

    %if %{with_qemu}
%ghost %dir %attr(0700, root, root) %{_localstatedir}/run/libvirt/qemu/
%dir %attr(0750, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/
%dir %attr(0750, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/channel/
%dir %attr(0750, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/channel/target/
%dir %attr(0750, %{qemu_user}, %{qemu_group}) %{_localstatedir}/cache/libvirt/qemu/
    %endif
    %if %{with_lxc}
%ghost %dir %{_localstatedir}/run/libvirt/lxc/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/lxc/
    %endif
    %if %{with_uml}
%ghost %dir %{_localstatedir}/run/libvirt/uml/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/uml/
    %endif
    %if %{with_libxl}
%ghost %dir %{_localstatedir}/run/libvirt/libxl/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/libxl/
    %endif
    %if %{with_xen}
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/xen/
    %endif
    %if %{with_network}
%ghost %dir %{_localstatedir}/run/libvirt/network/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/network/
%dir %attr(0755, root, root) %{_localstatedir}/lib/libvirt/dnsmasq/
    %endif

%dir %attr(0755, root, root) %{_libdir}/libvirt/lock-driver
%attr(0755, root, root) %{_libdir}/libvirt/lock-driver/lockd.so

    %if %{with_qemu}
%{_datadir}/augeas/lenses/libvirtd_qemu.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
    %endif

    %if %{with_lxc}
%{_datadir}/augeas/lenses/libvirtd_lxc.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_lxc.aug
    %endif

%{_datadir}/augeas/lenses/libvirtd.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd.aug
%{_datadir}/augeas/lenses/virtlockd.aug
%{_datadir}/augeas/lenses/tests/test_virtlockd.aug
%{_datadir}/augeas/lenses/libvirt_lockd.aug
%{_datadir}/augeas/lenses/tests/test_libvirt_lockd.aug

    %if %{with_polkit}
        %if 0%{?fedora} >= 12 || 0%{?rhel} >= 6 || 0%{?mcp} >= 7
%{_datadir}/polkit-1/actions/org.libvirt.unix.policy
        %else
%{_datadir}/PolicyKit/policy/org.libvirt.unix.policy
        %endif
    %endif

%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/

    %if %{with_lxc}
%attr(0755, root, root) %{_libexecdir}/libvirt_lxc
    %endif

    %if %{with_storage_disk}
%attr(0755, root, root) %{_libexecdir}/libvirt_parthelper
    %endif

%attr(0755, root, root) %{_libexecdir}/libvirt_iohelper
%attr(0755, root, root) %{_sbindir}/libvirtd
%attr(0755, root, root) %{_sbindir}/virtlockd

%{_mandir}/man8/libvirtd.8*
%{_mandir}/man8/virtlockd.8*

    %if %{with_driver_modules}
        %if %{with_network}
%files daemon-config-network
%defattr(-, root, root)
        %endif

        %if %{with_nwfilter}
%files daemon-config-nwfilter
%defattr(-, root, root)
%{_sysconfdir}/libvirt/nwfilter/*.xml
        %endif

        %if %{with_interface}
%files daemon-driver-interface
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_interface.so
        %endif

        %if %{with_network}
%files daemon-driver-network
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_network.so
        %endif

        %if %{with_nodedev}
%files daemon-driver-nodedev
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_nodedev.so
        %endif

        %if %{with_nwfilter}
%files daemon-driver-nwfilter
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_nwfilter.so
        %endif

%files daemon-driver-secret
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_secret.so

        %if %{with_storage}
%files daemon-driver-storage
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_storage.so
        %endif

        %if %{with_qemu}
%files daemon-driver-qemu
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_qemu.so
        %endif

        %if %{with_lxc}
%files daemon-driver-lxc
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_lxc.so
        %endif

        %if %{with_uml}
%files daemon-driver-uml
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_uml.so
        %endif

        %if %{with_xen}
%files daemon-driver-xen
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_xen.so
        %endif

        %if %{with_libxl}
%files daemon-driver-libxl
%defattr(-, root, root)
%{_libdir}/%{name}/connection-driver/libvirt_driver_libxl.so
        %endif
    %endif # %{with_driver_modules}

    %if %{with_qemu_tcg}
%files daemon-qemu
%defattr(-, root, root)
    %endif

    %if %{with_qemu_kvm}
%files daemon-kvm
%defattr(-, root, root)
    %endif

    %if %{with_lxc}
%files daemon-lxc
%defattr(-, root, root)
    %endif

    %if %{with_uml}
%files daemon-uml
%defattr(-, root, root)
    %endif

    %if %{with_xen} || %{with_libxl}
%files daemon-xen
%defattr(-, root, root)
    %endif
%endif # %{with_libvirtd}

%if %{with_sanlock}
%files lock-sanlock
%defattr(-, root, root)
    %if %{with_qemu}
%config(noreplace) %{_sysconfdir}/libvirt/qemu-sanlock.conf
    %endif
%attr(0755, root, root) %{_libdir}/libvirt/lock-driver/sanlock.so
%{_datadir}/augeas/lenses/libvirt_sanlock.aug
%{_datadir}/augeas/lenses/tests/test_libvirt_sanlock.aug
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/sanlock
%{_sbindir}/virt-sanlock-cleanup
%{_mandir}/man8/virt-sanlock-cleanup.8*
%attr(0755, root, root) %{_libexecdir}/libvirt_sanlock_helper
%endif

%files client -f %{name}.lang
%defattr(-, root, root)

%config(noreplace) %{_sysconfdir}/libvirt/libvirt.conf
%config(noreplace) %{_sysconfdir}/libvirt/virt-login-shell.conf

%{_mandir}/man1/virsh.1*
%{_mandir}/man1/virt-xml-validate.1*
%{_mandir}/man1/virt-pki-validate.1*
%{_mandir}/man1/virt-host-validate.1*
%{_mandir}/man1/virt-login-shell.1*
%{_bindir}/virsh
%{_bindir}/virt-xml-validate
%{_bindir}/virt-pki-validate
%{_bindir}/virt-host-validate
%attr(4755, root, root) %{_bindir}/virt-login-shell
%{_libdir}/lib*.so.*

%if %{with_dtrace}
%{_datadir}/systemtap/tapset/libvirt_probes*.stp
%{_datadir}/systemtap/tapset/libvirt_qemu_probes*.stp
%{_datadir}/systemtap/tapset/libvirt_functions.stp
%endif

%dir %{_datadir}/libvirt/
%dir %{_datadir}/libvirt/schemas/

%{_datadir}/libvirt/schemas/basictypes.rng
%{_datadir}/libvirt/schemas/capability.rng
%{_datadir}/libvirt/schemas/domain.rng
%{_datadir}/libvirt/schemas/domaincommon.rng
%{_datadir}/libvirt/schemas/domainsnapshot.rng
%{_datadir}/libvirt/schemas/interface.rng
%{_datadir}/libvirt/schemas/network.rng
%{_datadir}/libvirt/schemas/networkcommon.rng
%{_datadir}/libvirt/schemas/nodedev.rng
%{_datadir}/libvirt/schemas/nwfilter.rng
%{_datadir}/libvirt/schemas/secret.rng
%{_datadir}/libvirt/schemas/storageencryption.rng
%{_datadir}/libvirt/schemas/storagepool.rng
%{_datadir}/libvirt/schemas/storagevol.rng

%{_datadir}/libvirt/cpu_map.xml
%{_datadir}/libvirt/libvirtLogo.png

%if %{with_systemd}
%{_unitdir}/libvirt-guests.service
%else
%{_sysconfdir}/rc.d/init.d/libvirt-guests
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/libvirt-guests
%attr(0755, root, root) %{_libexecdir}/libvirt-guests.sh
%dir %attr(0755, root, root) %{_localstatedir}/lib/libvirt/

%if %{with_sasl}
%config(noreplace) %{_sysconfdir}/sasl2/libvirt.conf
%endif

%files devel
%defattr(-, root, root)

%{_libdir}/lib*.so
%dir %{_includedir}/libvirt
%{_includedir}/libvirt/*.h
%{_libdir}/pkgconfig/libvirt.pc

%dir %{_datadir}/libvirt/api/
%{_datadir}/libvirt/api/libvirt-api.xml
%{_datadir}/libvirt/api/libvirt-qemu-api.xml
%{_datadir}/libvirt/api/libvirt-lxc-api.xml

%doc docs/*.html docs/html docs/*.gif
%doc docs/libvirt-api.xml
%doc examples/hellolibvirt
%doc examples/domain-events/events-c
%doc examples/dominfo
%doc examples/domsuspend
%doc examples/openauth
%doc examples/xml
%doc examples/systemtap

%if %{with_python}
%files python
%defattr(-, root, root)

%doc TODO
%{_libdir}/python*/site-packages/libvirt.py*
%{_libdir}/python*/site-packages/libvirt_qemu.py*
%{_libdir}/python*/site-packages/libvirt_lxc.py*
%{_libdir}/python*/site-packages/libvirtmod*
%doc examples/python
%doc examples/domain-events/events-python
%endif

%if 0%{?mcp}
%{_datadir}/libvirt/schemas/storagefilefeatures.rng
%{_datadir}/polkit-1/actions/org.libvirt.api.policy
%endif


%changelog
* Tue Nov 26 2013 Wang Sen<wangsen@linux.vnet.ibm.com> 1.1.3-1.5
- Build5 update1: Fix for numatune to set node for live and current option
* Tue Nov 26 2013 Wang Sen<wangsen@linux.vnet.ibm.com> 1.1.3-1.5
- Modify the release format for pbuild5
* Wed Nov 20 2013 Wang Sen<wangsen@linux.vnet.ibm.com> 1.1.3-1
- Bump mcp_release to 4 for pbuild5.
* Wed Nov 20 2013 Wang Sen<wangsen@linux.vnet.ibm.com> 1.1.3-1
- Build parity x86 packages.
* Mon Nov 18 2013 Eli Qiao<qiaoly@cn.ibm.com> 1.1.3-1
- Fix migration with qemu 1.6(pbuild4 respin2)
* Fri Nov 08 2013 Wang Sen<wangsen@linux.vnet.ibm.com> 1.1.3-1
- KoP build4 update1: Include bug 99509 fix.
* Thu Oct 24 2013 Wang Sen <wangsen@linux.vnet.ibm.com> 1.1.3-1
- Build packages for KoP build4
* Wed Sep 25 2013 wangsen@linux.vnet.ibm.com 1.1.0-1
- Build KoP build3 packages.
* Tue Jul 09 2013 baseuser@ibm.com
- Base-8.x spec file
