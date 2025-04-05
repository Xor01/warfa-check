import Form from "next/form";
import { useTranslation } from "@/i18n";
export default async function ImageUploader() {
  const { t } = await useTranslation("index");
  return (
    <>
      <div className="flex flex-col gap-4">
        <h2 className="text-2xl font-bold">{t("uploadImage")}</h2>
        <Form action={"/upload"} className="">
          <input
            className="p-3 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer  w-70 min-w-70 max-w-80"
            style={{ backgroundColor: "var(--secondary)" }}
            id="file_input"
            type="file"
            accept="image/*"
          />
        </Form>
      </div>
    </>
  );
}
