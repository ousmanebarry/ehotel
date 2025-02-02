import { create } from "zustand";
import { HotelChainInfo } from "~/types";

interface UseHotelChains {
  hotelChains: HotelChainInfo[];
  setHotelChains: (hotelChains: HotelChainInfo[]) => void;
}

const useHotelChains = create<UseHotelChains>((set) => ({
  hotelChains: [],
  setHotelChains: (hotelChains: HotelChainInfo[]) =>
    set(() => ({ hotelChains })),
}));

export default useHotelChains;
