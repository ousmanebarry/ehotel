import { GetServerSideProps } from "next";
import "~/styles/globals.css";
import { AppProps } from "next/app";
import Head from "next/head";
import { MantineProvider } from "@mantine/core";

export default function App(props: AppProps) {
  const { Component, pageProps } = props;

  return (
    <>
      <Head>
        <title>E-hotels</title>
        <meta content="width=device-width, initial-scale=1" name="viewport" />
        <link
          rel="icon"
          href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🛏️</text></svg>"
        />
      </Head>

      <MantineProvider
        withGlobalStyles
        withNormalizeCSS
        theme={{
          colorScheme: "light",
        }}
      >
        <Component {...pageProps} />
      </MantineProvider>
    </>
  );
}

export const getServerSideProps: GetServerSideProps<{}> = async (context) => {
  const isLoggedIn = context.req.cookies["session_token"];

  if (!isLoggedIn) {
    return {
      redirect: { destination: "/login", permanent: false },
      props: {},
    };
  }

  return {
    props: {},
  };
};
