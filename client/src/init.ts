import {
  backButton,
  viewport,
  themeParams,
  miniApp,
  initData,
  closingBehavior,
  $debug,
  mainButton,
  init as initSDK,
} from '@telegram-apps/sdk-react';

/**
 * Initializes the application and configures its dependencies.
 */
export function init(debug: boolean): void {
  // Set @telegram-apps/sdk-react debug mode.
  $debug.set(debug);

  // Initialize special event handlers for Telegram Desktop, Android, iOS, etc.
  // Also, configure the package.
  initSDK();

  // Check if all required components are supported.
  if (!backButton.isSupported() || !miniApp.isSupported()) {
    throw new Error('ERR_NOT_SUPPORTED');
  }

  if (mainButton.mount.isAvailable()) {
    mainButton.mount();
    mainButton.isMounted(); // true
    mainButton.setParams({
      backgroundColor: '#0096FF',
      hasShineEffect: true,
      isEnabled: true,
      isLoaderVisible: false,
      isVisible: false,
      text: 'My text',
      textColor: '#ffffff',
    });
  }

  if (closingBehavior.mount.isAvailable()) {
    closingBehavior.mount();
    console.log(closingBehavior.isMounted()); // true
    closingBehavior.enableConfirmation();
    console.log(closingBehavior.isConfirmationEnabled()); // true
  }

  // Mount all components used in the project.
  backButton.mount();
  miniApp.mount();
  themeParams.mount();
  initData.restore();
  void viewport
    .mount()
    .catch((e) => {
      console.error('Something went wrong mounting the viewport', e);
    })
    .then(() => {
      viewport.bindCssVars();
    });
  // backButton.show();
  // backButton.onClick(() => {
  //   console.log('Back button clicked');
  // });
  // backButton.hide();
}
