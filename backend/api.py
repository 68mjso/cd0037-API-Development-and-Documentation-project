from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
from models import Question, Category
import random

api = Blueprint("api", __name__)

QUESTIONS_PER_PAGE = 10


@api.route("/categories", methods=["GET"])
@cross_origin()
def get_categories():
    categories = Category.query.all()
    cate_dict = {category.id: category.type for category in categories}
    return jsonify({"status": 200, "categories": cate_dict}), 200


@api.route("/questions", methods=["GET"])
@cross_origin()
def get_questions():
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * QUESTIONS_PER_PAGE
    result = (
        Question.query.order_by(Question.id)
        .limit(QUESTIONS_PER_PAGE)
        .offset(offset)
        .all()
    )
    total_questions = len(Question.query.all())
    categories = Category.query.all()
    quest_dict = [question.format() for question in result]
    cate_dict = {category.id: category.type for category in categories}
    return (
        jsonify(
            {
                "status": 200,
                "questions": quest_dict,
                "total_questions": total_questions,
                "categories": cate_dict,
                "current_category": "All",
            }
        ),
        200,
    )


@api.route("/questions/<int:id>", methods=["PUT"])
@cross_origin()
def put_question(id):
    quest: Question = Question.query.get(id)
    if quest is None:
        return jsonify({"status": 404, "message": "Question not found."}), 404
    data = request.json
    question = data.get("question")
    answer = data.get("answer")
    difficulty = data.get("difficulty")
    category = data.get("category")
    if question is None or answer is None or difficulty is None or category is None:
        return jsonify({"status": 400, "message": "Missing required params."}), 400
    quest.question = question
    quest.answer = answer
    quest.difficulty = difficulty
    quest.category = category
    quest.update()

    return jsonify({"status": 200, "message": "Success"}), 200


@api.route("/questions/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_question(id):
    question = Question.query.get(id)
    if question is None:
        return jsonify({"status": 404, "message": "Question not found"}), 404
    question.delete()

    return jsonify({"status": 200, "message": "Success"}), 200


@api.route("/questions", methods=["POST"])
@cross_origin()
def add_question():
    try:
        data = request.json
        question = data.get("question")
        answer = data.get("answer")
        difficulty = data.get("difficulty")
        category = data.get("category")
        if question is None or answer is None or difficulty is None or category is None:
            return jsonify({"status": 400, "message": "Missing required params."}), 400
        q = Question(
            question=question,
            answer=answer,
            difficulty=difficulty,
            category=category,
        )
        q.insert()
    except Exception as e:
        return jsonify({"status": 400, "message": "Add Question Failed"}), 400

    return jsonify({"status": 200, "message": "Success"}), 200


@api.route("/questions/search", methods=["POST"])
@cross_origin()
def search_question():
    search_term = request.json.get("searchTerm")
    if search_term is None:
        return (
            jsonify({"status": 400, "message": "Missing search term."}),
            400,
        )
    questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
    data = [question.format() for question in questions]
    total_questions = len(data)
    return (
        jsonify(
            {
                "status": 200,
                "questions": data,
                "total_questions": total_questions,
                "current_category": "All",
            }
        ),
        200,
    )


@api.route("/categories/<int:id>/questions", methods=["GET"])
@cross_origin()
def get_categories_questions(id):
    category = Category.query.get(id)
    if category is None:
        return (jsonify({"status": 404, "message": "Category not found."}), 404)
    data = []
    result = (
        Question.query.join(Category, Question.category == Category.id)
        .where(Category.id == id)
        .all()
    )
    total_questions = len(result)
    category = Category.query.get(id)
    for question in result:
        data.append(question.format())
    return (
        jsonify(
            {
                "status": 200,
                "questions": data,
                "total_questions": total_questions,
                "current_category": category.type,
            }
        ),
        200,
    )


@api.route("/quizzes", methods=["POST"])
@cross_origin()
def get_quizzes():
    previous_questions = request.json.get("previous_questions")
    quiz_category = request.json.get("quiz_category")
    if previous_questions is None or quiz_category is None:
        return (jsonify({"status": 400, "message": "Missing required params."}), 400)
    data = []
    if quiz_category["id"] == 0:
        result = Question.query.all()
    else:
        result = (
            Question.query.join(Category, Question.category == Category.id)
            .where(Category.id == quiz_category["id"])
            .all()
        )
    for question in result:
        data.append(question.format())
    filtered_data = [item for item in data if item["id"] not in previous_questions]
    if len(filtered_data) == 0:
        return jsonify({"status": 200, "question": None})
    rand = random.randint(0, len(filtered_data) - 1)

    return jsonify({"status": 200, "question": filtered_data[rand]})
