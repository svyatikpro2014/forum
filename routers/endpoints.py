from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from database import get_session
from models import PostsModel
from schemas import PostAddSchema, PostResponse, PostUpdate



router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostResponse])
async def get_posts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PostsModel))
    return result.scalars().all()


@router.post("/", response_model=PostAddSchema)
async def add_post(post:PostAddSchema,session: AsyncSession = Depends(get_session)):
    db_post = PostsModel(**post.dict())
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post) #to be able to return an object with its id later
    return db_post

@router.delete("/{post_id}")
async def delete_post(post_id: int ,session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PostsModel).where(PostsModel.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="not found")
    
    await session.delete(post)
    await session.commit()
    return {"ok": True}

@router.patch("/{post_id}")
async def edit_post(post_id: int, post_update:PostUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PostsModel).where(PostsModel.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="not found")
    
    await session.execute(update(PostsModel).where(PostsModel.id == post_id).values(**post_update.dict()))
    await session.commit()
    await session.refresh(post)
    return post