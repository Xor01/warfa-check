import { useTranslation } from "@/i18n";
import ImageUploader from "@/components/ImageUploader";
import NameSearch from "./NameSearch";
export default async function MainForm() {
  const { t } = await useTranslation("index");
  return (
    <>
      <div className="flex flex-col justify-start items-center h-screen gap-10 mt-5">
        <h1 className="text-sm lg:text-3xl font-bold">{t("heading")}</h1>
        <ImageUploader />
        <NameSearch />
      </div>
    </>
  );
}
