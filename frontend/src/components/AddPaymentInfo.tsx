import Payment from "payment";
import { useDisclosure } from "@mantine/hooks";
import { useForm, isNotEmpty } from "@mantine/form";
import { Modal, Button, TextInput, Group, Stack } from "@mantine/core";
import { message } from "antd";

interface AddPaymentInfoProps {
  complete: boolean;
  setComplete: () => void;
}

export default function AddPaymentInfo({
  complete,
  setComplete,
}: AddPaymentInfoProps) {
  const [opened, { open, close }] = useDisclosure(false);

  const form = useForm({
    initialValues: {
      name: "",
      cardNumber: "",
      csv: "",
      expiry: "",
    },
    validate: {
      name: isNotEmpty("Enter your name"),
      cardNumber(value) {
        if (Payment.fns.validateCardNumber(value)) {
          return null;
        }

        return "Invalid credit card number";
      },
      csv(value) {
        if (Payment.fns.validateCardCVC(value)) {
          return null;
        }

        return "Invalid csv";
      },
      expiry(value) {
        if (Payment.fns.validateCardExpiry(value)) {
          return null;
        }

        return "Invalid expiry";
      },
    },
  });

  const handleSubmit = form.onSubmit(() => {
    message.success("Added payment info");
    setComplete();
    close();
  });

  return (
    <>
      <Modal opened={opened} onClose={close} title="Add Payment Info">
        <Stack spacing="md" sx={{ padding: "20px 50px" }}>
          <TextInput
            placeholder="Credit Card Name"
            label="Credit Card Name"
            {...form.getInputProps("name")}
          />
          <TextInput
            ref={(element) => {
              if (element) Payment.formatCardNumber(element);
            }}
            placeholder="#### #### #### ####"
            label="Card Number"
            {...form.getInputProps("cardNumber")}
          />

          <Group align="center">
            <TextInput
              ref={(element) => {
                if (element) Payment.formatCardCVC(element);
              }}
              placeholder="###"
              label="CSV"
              {...form.getInputProps("csv")}
            />
            <TextInput
              ref={(element) => {
                if (element) Payment.formatCardExpiry(element);
              }}
              placeholder="MM / YYYY"
              label="Expiry"
              {...form.getInputProps("expiry")}
            />
          </Group>
          <Button onClick={handleSubmit as any}>Submit</Button>
        </Stack>
      </Modal>

      <Button onClick={open} disabled={complete}>
        {!complete ? "Add Payment" : "Complete"}
      </Button>
    </>
  );
}
