import "./reviewCard.css";
import avatarImage from "../../avatarImage.json";


function reviewCard({ review }) {
    const { star, fullName, classSchool, text, avatar } = review;
    const stars = Array.from({ length: star }, (_, index) => (
        <img key={index} src="/star.png" alt="" />  /* создание массива звезд чтобы при определении
  количества звезд из json отображать это количества */
    ))
    const currentAvatar = avatarImage.avatars.find((item) => item.id === avatar)


    return (
        <div className="review">
            <div className="text">
                <div className="stars">
                    {stars}
                </div>
                <p>{text}</p>
                <div className="user">
                    {
                        currentAvatar ? <img src={currentAvatar.image} alt={currentAvatar.name} /> : null
                    }
                    <div className="nameUser">
                        <h3>{fullName}</h3>
                        <p>{classSchool}</p>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default reviewCard;