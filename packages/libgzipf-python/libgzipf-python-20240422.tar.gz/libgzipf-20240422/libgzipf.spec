Name: libgzipf
Version: 20240422
Release: 1
Summary: Library to access the GZIP file format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libgzipf
Requires:              zlib
BuildRequires: gcc              zlib-devel

%description -n libgzipf
Library to access the GZIP file format

%package -n libgzipf-static
Summary: Library to access the GZIP file format
Group: Development/Libraries
Requires: libgzipf = %{version}-%{release}

%description -n libgzipf-static
Static library version of libgzipf.

%package -n libgzipf-devel
Summary: Header files and libraries for developing applications for libgzipf
Group: Development/Libraries
Requires: libgzipf = %{version}-%{release}

%description -n libgzipf-devel
Header files and libraries for developing applications for libgzipf.

%package -n libgzipf-python3
Summary: Python 3 bindings for libgzipf
Group: System Environment/Libraries
Requires: libgzipf = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libgzipf-python3
Python 3 bindings for libgzipf

%package -n libgzipf-tools
Summary: Several tools for reading GZIP files
Group: Applications/System
Requires: libgzipf = %{version}-%{release} fuse3-libs
BuildRequires: fuse3-devel

%description -n libgzipf-tools
Several tools for reading GZIP files

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libgzipf
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libgzipf-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libgzipf-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libgzipf.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libgzipf-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libgzipf-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Apr 22 2024 Joachim Metz <joachim.metz@gmail.com> 20240422-1
- Auto-generated

