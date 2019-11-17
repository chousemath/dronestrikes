module Main exposing (Model, Msg(..), init, main, update, view)

import Browser
import Html exposing (Html, button, div, text)
import Html.Events exposing (onClick)



-- MAIN


main =
    Browser.sandbox
        { init = init
        , update = update
        , view = view
        }


type alias Model =
    { x : Int
    , y : Int
    , z : Int
    }


init : Model
init =
    { x = 0
    , y = 0
    , z = 0
    }



-- UPDATE


type Msg
    = Alter String String


update : Msg -> Model -> Model
update msg model =
    case msg of
        Alter var cmd ->
            case var of
                "x" ->
                    case cmd of
                        "add" ->
                            { model | x = model.x + 1 }

                        "sub" ->
                            { model | x = model.x - 1 }

                        _ ->
                            { model | x = 0 }

                "y" ->
                    case cmd of
                        "add" ->
                            { model | y = model.y + 1 }

                        "sub" ->
                            { model | y = model.y - 1 }

                        _ ->
                            { model | y = 0 }

                "z" ->
                    case cmd of
                        "add" ->
                            { model | z = model.z + 1 }

                        "sub" ->
                            { model | z = model.z - 1 }

                        _ ->
                            { model | z = 0 }

                _ ->
                    { model | x = 0 }



-- VIEW


view : Model -> Html Msg
view model =
    div []
        [ button [ onClick (Alter "x" "sub") ] [ text "--x" ]
        , button [ onClick (Alter "y" "sub") ] [ text "--y" ]
        , button [ onClick (Alter "z" "sub") ] [ text "--z" ]
        , button [ onClick (Alter "x" "add") ] [ text "++x" ]
        , button [ onClick (Alter "y" "add") ] [ text "++y" ]
        , button [ onClick (Alter "z" "add") ] [ text "++z" ]
        , div [] [ text ("x: " ++ String.fromInt model.x) ]
        , div [] [ text ("y: " ++ String.fromInt model.y) ]
        , div [] [ text ("z: " ++ String.fromInt model.z) ]
        ]
