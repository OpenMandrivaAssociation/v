# yeah, the library is called "v" .... 
%define name		v
%define version		1.90
%define release		%mkrel 4
%define major		1.90
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Multiple platform C++ graphical user interface framework
License:	LGPL
Group:		Development/C++
Source0:	%{name}-%{version}.tar.bz2
Patch0:		v-gcc41.patch.bz2
URL:		http://www.objectcentral.com/
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	lesstif-devel, X11-devel

%description
V is a free, multiple platform C++ graphical user interface framework designed
to make it the easiest way to write C++ GUI applications available -- 
commercial, shareware, or freeware. V is available for X Athena, 
X Motif/Lesstif, all Windows platforms, and now including OS/2.

%package -n %{libname}
Summary:        Main library for %{name}
Group:          System/Libraries
Provides:       lib%{name} = %{version}-%{release}

%description -n %{libname}
V is a free, multiple platform C++ graphical user interface framework designed
to make it the easiest way to write C++ GUI applications available --
commercial, shareware, or freeware. V is available for X Athena,
X Motif/Lesstif, all Windows platforms, and now including OS/2.


%package -n %{develname}
Summary:        Development header files for %{name}
Group:          Development/C++
Requires:       %{libname} = %{version}
Provides:       lib%{name}-devel = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname v 1.90 -d}

%description -n %{develname}
Libraries, include files and other resources you can use to develop
%{name} applications.

%prep
%setup -q -n home/vgui
%patch0
%build

perl -pi -e "s|^HOMEV\s*=.*|HOMEV=`pwd`|" Config.mk
perl -pi -e "s|^ARCH\s*=.*|ARCH = linuxelf|" Config.mk
perl -pi -e "s|^TOOLKIT\s*=.*|TOOLKIT = Athena|" Config.mk
perl -pi -e "s|^NeedGLw\s*=.*|NeedGLw = no|" Config.mk
perl -pi -e "s|^LIBDIR\s*\+=\s*-L/usr/.*/lib|LIBDIR \+= -L%{_prefix}/\\$\(X11RV\)/%{_lib}|" Config.mk
perl -pi -e 's|GLw/GLwMDrawA.h|GL/GLwMDrawA.h|' srcx/vbglcnv.cxx
perl -pi -e 's|GLw/GLwDrawA.h|GL/GLwDrawA.h|' srcx/vbglcnv.cxx
perl -pi -e "s|-rm|rm|" srcx/Makefile
perl -pi -e "s|-ln|ln|" srcx/Makefile

export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"

# parallel build fail
make 

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}

cp lib/lib* $RPM_BUILD_ROOT%{_libdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libVx.so
ln -s %{_libdir}/libVx.so.1.90 $RPM_BUILD_ROOT%{_libdir}/libVx.so
ln -s %{_libdir}/libVxgl.so.1.90 $RPM_BUILD_ROOT%{_libdir}/libVxgl.so

cp -r includex/* $RPM_BUILD_ROOT%{_includedir}

perl -pi -e "s|\r\n|\n|" $RPM_BUILD_ROOT%{_includedir}/v/*
perl -pi -e "s|\r\n|\n|"  ../help/vrefman/* Readme copying.lib

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %{libname}
%defattr (755,root,root)
%doc Readme copying.lib
%{_libdir}/*.so.*

%files -n %{develname}
%defattr (-,root,root,755)
%doc ../help/vrefman/*
%{_includedir}/%{name}
%{_libdir}/*.so
