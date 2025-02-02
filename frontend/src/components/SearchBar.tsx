import { TextInput } from "@mantine/core";
import { IconSearch } from "@tabler/icons";
import useSearchQuery from "~/utils/useSearchQuery";

export default function SearchBar() {
  const [location, setSearchQuery] = useSearchQuery((state) => [
    state.location,
    state.setQuery,
  ]);

  return (
    <TextInput
      value={location}
      onChange={(event) => {
        setSearchQuery({ location: event.target.value });
      }}
      placeholder="Destination"
      icon={<IconSearch />}
      radius="xl"
      sx={{
        boxShadow: "rgba(0, 0, 0, 0.08) 0px 1px 2px",
        borderRadius: "32px",
        width: "400px",
      }}
    />
  );
}
