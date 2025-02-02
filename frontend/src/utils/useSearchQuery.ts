import { create } from "zustand";

interface SearchQuery {
  startDate: string;
  endDate: string;
  price: null | number;
  hotelChain: null | string;
  category: null | number;
  roomCapacity: string;
  location: string;
  setDateRange: (dateRange: string[]) => void;
  setQuery: (query: SearchQueryOptional) => void;
}

interface SearchQueryOptional {
  startDate?: string;
  endDate?: string;
  price?: null | number;
  hotelChain?: null | string;
  category?: null | number;
  roomCapacity?: string;
  location?: string;
}

const useSearchQuery = create<SearchQuery>((set) => ({
  startDate: "",
  endDate: "",
  price: null,
  hotelChain: null,
  category: null,
  roomCapacity: "any",
  location: "",
  setDateRange: (dateRange: string[]) =>
    set((state) => ({
      ...state,
      startDate: dateRange[0],
      endDate: dateRange[1],
    })),
  setQuery: (query: SearchQueryOptional) =>
    set((state) => ({ ...state, ...query })),
}));

export default useSearchQuery;
