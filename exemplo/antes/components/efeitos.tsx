// Três efeitos de exemplo, todos ligados na mesma página.
export const Meteors = () => <div className="animate-meteor" />;
export const Marquee = ({ children }: { children: React.ReactNode }) => (
  <div className="animate-marquee">{children}</div>
);
export const BorderBeam = () => <div className="borda-animada" />;
