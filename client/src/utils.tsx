export const getConnectWalletTask = (categories: Array<any>) => {
  const connectWalletCategory = categories.find(
    (category: any) => category.title === 'Connect Wallet'
  );
  const connectWalletBranch = connectWalletCategory?.branches.find(
    (branch: any) => branch.title === 'Connect Wallet'
  );
  const connectWalletTask = connectWalletBranch?.tasks.find(
    (task: any) => task.task_type === 'connect_wallet'
  );
  return connectWalletTask;
};
