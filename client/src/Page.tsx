import { useNavigate } from 'react-router-dom';
import { backButton, mainButton } from '@telegram-apps/sdk-react';
import { PropsWithChildren, useEffect } from 'react';
import React from 'react';

export function Page({
  children,
  back = true,
  disableMainButton = false,
}: PropsWithChildren<{
  /**
   * True if it is allowed to go back from this page.
   */
  back?: boolean;
  /**
   * True if the main button should be disabled.
   */
  disableMainButton?: boolean;
}>) {
  useEffect(() => {
    if (disableMainButton) {
      mainButton.setParams({
        isVisible: false,
      });
      return mainButton.onClick(() => {});
    }
  }, [disableMainButton]);
  const navigate = useNavigate();

  useEffect(() => {
    if (back) {
      backButton.show();
      return backButton.onClick(() => {
        navigate(-1);
      });
    }
    backButton.hide();
  }, [back]);

  return <>{children}</>;
}
