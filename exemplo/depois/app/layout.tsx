import { Fraunces, Source_Sans_3 } from "next/font/google";
import { Toaster } from "sonner";
import "./globals.css";

const titulo = Fraunces({ subsets: ["latin"], variable: "--font-titulo" });
const corpo = Source_Sans_3({ subsets: ["latin"], variable: "--font-corpo" });

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" className={`${titulo.variable} ${corpo.variable}`}>
      <body>
        {children}
        <Toaster position="bottom-center" />
      </body>
    </html>
  );
}
