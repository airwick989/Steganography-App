import React from 'react';
import { ReactComponent as LogoutSVG } from '../../assets/logout.svg';

const LogoutIcon = ({ width, height, fill }) => {
  return <LogoutSVG width={width} height={height} fill={fill} />;
};

export default LogoutIcon;