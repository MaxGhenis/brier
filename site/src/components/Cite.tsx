export function Cite({ id, children }: { id: string; children: React.ReactNode }) {
  return (
    <sup className="text-[0.75em] align-super leading-none">
      <a
        href={`#ref-${id}`}
        id={`cite-${id}`}
        className="text-accent no-underline px-[0.1em] hover:underline"
      >
        [{children}]
      </a>
    </sup>
  );
}
