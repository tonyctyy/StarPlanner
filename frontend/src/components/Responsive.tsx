/**
 * Responsive.tsx
 * 
 * Implements responsive components for different device sizes.
 * 
 * Has Phone, Tablet, Desktop components.
 * Exposes useDeviceSizes and getSize hooks.
 * 
 * @key Phone, Tablet, Desktop components 
 * @key useDeviceSizes hook
 * @key getSize hook
*/


import React from "react";
import { useMediaQuery } from "react-responsive";

interface DeviceSizes {
    isPhone: boolean;
    isTablet: boolean;
    isDesktop: boolean;
}

export const useDeviceSizes = (): DeviceSizes => {
    const isPhone = useMediaQuery({ query: '(max-width: 576px)' });
    const isTablet = useMediaQuery({ query: '(min-width: 577px) and (max-width: 992px)' });
    const isDesktop = useMediaQuery({ query: '(min-width: 993px)' });

    return {
        isPhone,
        isTablet,
        isDesktop
    };
};

export const Phone = ({ children }: { children: React.ReactNode }) => {
    const { isPhone } = useDeviceSizes();
    return isPhone ? <>{children}</> : null;
};

export const Tablet = ({ children }: { children: React.ReactNode }) => {
    const { isTablet } = useDeviceSizes();
    return isTablet ? <>{children}</> : null;
};

export const Desktop = ({ children }: { children: React.ReactNode }) => {
    const { isDesktop } = useDeviceSizes();
    return isDesktop ? <>{children}</> : null;
};

export function getSize() {
    const { isPhone, isTablet, isDesktop } = useDeviceSizes();
    if (isPhone) {
        return 'phone';
    }
    if (isTablet) {
        return 'tablet';
    }
    if (isDesktop) {
        return 'desktop';
    }
}