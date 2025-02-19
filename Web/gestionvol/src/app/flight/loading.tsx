import style from "./listflight.module.css"
export default function Loading()
{
    return(
        <>
        <div className={style.loading}>
            <h1>LOADING...</h1>
        </div>
        </>
    );
}