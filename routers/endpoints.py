from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from database import get_session
from models import PostsModel, UsersModel
from schemas import PostAddSchema, PostResponse, PostUpdate
from routers.auth import get_user



router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostResponse])
async def get_posts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PostsModel))
    return result.scalars().all()


@router.post("/", response_model=PostResponse)
async def add_post(post: PostAddSchema, current_user = Depends(get_user), session: AsyncSession = Depends(get_session)):
    db_post = PostsModel(**post.dict(), user_id = current_user.id, user=current_user)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post

@router.delete("/{post_id}")
async def delete_post(post_id: int, current_user = Depends(get_user), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PostsModel).where(PostsModel.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="not found")
    
    if current_user.id != post.user_id and current_user.role != "Moderator":
        raise HTTPException(status_code=403, detail="Not allowed")
    
    await session.delete(post)
    await session.commit()
    return {"ok": True}

@router.patch("/{post_id}")
async def edit_post(post_update: PostUpdate, post_id: int, current_user = Depends(get_user), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PostsModel).where(PostsModel.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="not found")
    
    if current_user.id != post.user_id and current_user.role != "Moderator":
        raise HTTPException(status_code=403, detail="Not allowed")
    
    await session.execute(update(PostsModel).where(PostsModel.id == post_id).values(**post_update.dict()))
    await session.commit()
    await session.refresh(post)
    return post