import React, {useEffect, useState} from 'react';
import NavbarNavLink from '@theme-original/NavbarItem/NavbarNavLink';

export default function NavbarNavLinkWrapper(props) {
  const [authenticated, setAuthenticated] = useState(false);
  useEffect(() => {
    setAuthenticated(window.__simpoAuthenticated === true);
    const update = event => setAuthenticated(event.detail === true);
    window.addEventListener('simpo-auth-changed', update);
    return () => window.removeEventListener('simpo-auth-changed', update);
  }, []);
  if ((props.docspluginid === 'Dashboard' && !authenticated) ||
      (props.docspluginid === 'SignIn' && authenticated)) return null;
  return <NavbarNavLink {...props} />;
}
