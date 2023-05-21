import React, { useEffect } from 'react';
import NavbarNavLink from '@theme-original/NavbarItem/NavbarNavLink';

export default function NavbarNavLinkWrapper(props) {


  const { docsPluginId } = props;
  let ifSign;

  useEffect(() => {
    ifSign = localStorage.getItem('ifSign');
    console.log(localStorage.getItem('ifSign'));
    console.log(ifSign);
    // if (docsPluginId === 'Dashboard' && localStorage.getItem('ifSign') !== 'true') {
    //   return null;
    // }
    // if (docsPluginId === 'SignIn' && localStorage.getItem('ifSign') === 'true') {
    //   return null;
    // }
  });

  console.log(ifSign);

  if (docsPluginId === 'Dashboard' && ifSign !== 'true') {
    return null;
  }
  if (docsPluginId === 'SignIn' && ifSign === 'true') {
    return null;
  }
  console.log(ifSign);


  return (
    <>
      <NavbarNavLink {...props} />
    </>
  );
}
