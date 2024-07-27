import ClientSideProvider from "../providers";

const RootStorefrontLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <ClientSideProvider>
      {children}
    </ClientSideProvider>
  );
}

export default RootStorefrontLayout;