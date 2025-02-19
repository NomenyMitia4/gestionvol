import Link from "next/link"
import homeStyle from "./home.module.css"

export default function Home()
{
  return(
    <>
      <div className={homeStyle.header}>
        <h3>Flight Madagascar</h3>
      </div>
      <div className={homeStyle.content}>
        <h1>Manage your Flight</h1>
        <Link href={"/flight"}>
          <button className={homeStyle.btnTravel}>Travel Now</button>
        </Link>
      </div>
    </>
  )
}