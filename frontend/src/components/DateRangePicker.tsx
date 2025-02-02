"use client";

import { useEffect, useLayoutEffect, useState } from "react";
import dayjs from "dayjs";

import {
  Flex,
  Popover,
  Text,
  UnstyledButton,
  Center,
  Divider,
} from "@mantine/core";
import { RangeCalendar } from "@mantine/dates";
import { Calendar } from "react-feather";

type DateRange = [Date | null, Date | null];

function formatDate(date: Date | null) {
  return !date ? "---, --/--/--" : dayjs(date).format("ddd, MM/DD/YY");
}

interface DateRangePickerProps {
  startDateLabel?: string;
  endDateLabel?: string;
  setDateRange?: (dateRange: string[]) => void;
}

export default function DateRangePicker(props: DateRangePickerProps) {
  const [dateRange, setDateRange] = useState<DateRange>([null, null]);

  useEffect(() => {
    const startDate = dateRange[0]
      ? dayjs(dateRange[0]).format("YYYY-MM-DD")
      : "";
    const endDate = dateRange[1]
      ? dayjs(dateRange[1]).format("YYYY-MM-DD")
      : "";

    if (props.setDateRange) props.setDateRange([startDate, endDate]);
  }, [dateRange, props.setDateRange]);

  useLayoutEffect(() => {
    if (dateRange[0] && (!dateRange[1] || dateRange[0] > dateRange[1])) {
      const newValue = [new Date(dateRange[0]), new Date(dateRange[0])];
      newValue[1].setDate(newValue[0].getDate() + 1);

      setDateRange(newValue as DateRange);
    }
  }, [dateRange]);

  return (
    <Flex sx={{ width: "300px" }}>
      <Popover position="bottom" withArrow shadow="md">
        <Popover.Target>
          <UnstyledButton>
            <Center inline>
              <Flex direction="column" sx={{ paddingRight: "8px" }}>
                {props.startDateLabel && (
                  <Text size="xs">{props.startDateLabel}</Text>
                )}
                <Text size={!dateRange[0] ? "md" : "sm"}>
                  {formatDate(dateRange[0])}
                </Text>
              </Flex>
              <Calendar />
            </Center>
          </UnstyledButton>
        </Popover.Target>

        <Popover.Dropdown>
          <RangeCalendar
            value={dateRange}
            onChange={setDateRange}
            weekendDays={[]}
            minDate={new Date()}
            initialMonth={dateRange[0] || new Date()}
            hideOutsideDates
          />
        </Popover.Dropdown>
      </Popover>

      <Divider orientation="vertical" sx={{ margin: "0px 16px" }} />

      <Popover position="bottom" withArrow shadow="md">
        <Popover.Target>
          <UnstyledButton>
            <Center inline>
              <Flex direction="column" sx={{ paddingRight: "8px" }}>
                {props.endDateLabel && (
                  <Text size="xs">{props.endDateLabel}</Text>
                )}
                <Text size={!dateRange[1] ? "md" : "sm"}>
                  {formatDate(dateRange[1])}
                </Text>
              </Flex>
              <Calendar />
            </Center>
          </UnstyledButton>
        </Popover.Target>

        <Popover.Dropdown>
          <RangeCalendar
            value={dateRange}
            onChange={setDateRange}
            weekendDays={[]}
            minDate={new Date()}
            initialMonth={dateRange[1] || new Date()}
            hideOutsideDates
          />
        </Popover.Dropdown>
      </Popover>
    </Flex>
  );
}
