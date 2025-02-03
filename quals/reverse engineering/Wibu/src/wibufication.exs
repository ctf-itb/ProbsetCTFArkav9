defmodule Wibufication do
  defp convert(s) do
    String.codepoints(s)
    |> Enum.chunk_every(2, 2, [])
    |> Enum.map_join(& &1 |> process_chunk())
  end

  defp process_chunk([c1, c2]) do
    :binary.first(c1)
    |> Kernel.*(128)
    |> Kernel.+(:binary.first(c2))
    |> Kernel.+(0x4e00)
    |> then(fn x -> <<x::utf8>> end)
  end

  defp process_chunk([c1]) do
    process_chunk([c1, "\x00"])
  end

  def main() do
    System.argv()
    |> Enum.join(" ")
    |> convert()
    |> IO.puts()
  end
end
