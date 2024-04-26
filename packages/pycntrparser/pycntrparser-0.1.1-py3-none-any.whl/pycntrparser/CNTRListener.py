# Generated from CNTR.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .CNTRParser import CNTRParser
else:
    from CNTRParser import CNTRParser

# This class defines a complete listener for a parse tree produced by CNTRParser.
class CNTRListener(ParseTreeListener):

    # Enter a parse tree produced by CNTRParser#start.
    def enterStart(self, ctx:CNTRParser.StartContext):
        pass

    # Exit a parse tree produced by CNTRParser#start.
    def exitStart(self, ctx:CNTRParser.StartContext):
        pass


    # Enter a parse tree produced by CNTRParser#line.
    def enterLine(self, ctx:CNTRParser.LineContext):
        pass

    # Exit a parse tree produced by CNTRParser#line.
    def exitLine(self, ctx:CNTRParser.LineContext):
        pass


    # Enter a parse tree produced by CNTRParser#lines.
    def enterLines(self, ctx:CNTRParser.LinesContext):
        pass

    # Exit a parse tree produced by CNTRParser#lines.
    def exitLines(self, ctx:CNTRParser.LinesContext):
        pass


    # Enter a parse tree produced by CNTRParser#letter.
    def enterLetter(self, ctx:CNTRParser.LetterContext):
        pass

    # Exit a parse tree produced by CNTRParser#letter.
    def exitLetter(self, ctx:CNTRParser.LetterContext):
        pass


    # Enter a parse tree produced by CNTRParser#symbol.
    def enterSymbol(self, ctx:CNTRParser.SymbolContext):
        pass

    # Exit a parse tree produced by CNTRParser#symbol.
    def exitSymbol(self, ctx:CNTRParser.SymbolContext):
        pass


    # Enter a parse tree produced by CNTRParser#character.
    def enterCharacter(self, ctx:CNTRParser.CharacterContext):
        pass

    # Exit a parse tree produced by CNTRParser#character.
    def exitCharacter(self, ctx:CNTRParser.CharacterContext):
        pass


    # Enter a parse tree produced by CNTRParser#break.
    def enterBreak(self, ctx:CNTRParser.BreakContext):
        pass

    # Exit a parse tree produced by CNTRParser#break.
    def exitBreak(self, ctx:CNTRParser.BreakContext):
        pass


    # Enter a parse tree produced by CNTRParser#breaks.
    def enterBreaks(self, ctx:CNTRParser.BreaksContext):
        pass

    # Exit a parse tree produced by CNTRParser#breaks.
    def exitBreaks(self, ctx:CNTRParser.BreaksContext):
        pass


    # Enter a parse tree produced by CNTRParser#remnant.
    def enterRemnant(self, ctx:CNTRParser.RemnantContext):
        pass

    # Exit a parse tree produced by CNTRParser#remnant.
    def exitRemnant(self, ctx:CNTRParser.RemnantContext):
        pass


    # Enter a parse tree produced by CNTRParser#remnants.
    def enterRemnants(self, ctx:CNTRParser.RemnantsContext):
        pass

    # Exit a parse tree produced by CNTRParser#remnants.
    def exitRemnants(self, ctx:CNTRParser.RemnantsContext):
        pass


    # Enter a parse tree produced by CNTRParser#suffix.
    def enterSuffix(self, ctx:CNTRParser.SuffixContext):
        pass

    # Exit a parse tree produced by CNTRParser#suffix.
    def exitSuffix(self, ctx:CNTRParser.SuffixContext):
        pass


    # Enter a parse tree produced by CNTRParser#modifier.
    def enterModifier(self, ctx:CNTRParser.ModifierContext):
        pass

    # Exit a parse tree produced by CNTRParser#modifier.
    def exitModifier(self, ctx:CNTRParser.ModifierContext):
        pass


    # Enter a parse tree produced by CNTRParser#supplied.
    def enterSupplied(self, ctx:CNTRParser.SuppliedContext):
        pass

    # Exit a parse tree produced by CNTRParser#supplied.
    def exitSupplied(self, ctx:CNTRParser.SuppliedContext):
        pass


    # Enter a parse tree produced by CNTRParser#word.
    def enterWord(self, ctx:CNTRParser.WordContext):
        pass

    # Exit a parse tree produced by CNTRParser#word.
    def exitWord(self, ctx:CNTRParser.WordContext):
        pass


    # Enter a parse tree produced by CNTRParser#head.
    def enterHead(self, ctx:CNTRParser.HeadContext):
        pass

    # Exit a parse tree produced by CNTRParser#head.
    def exitHead(self, ctx:CNTRParser.HeadContext):
        pass


    # Enter a parse tree produced by CNTRParser#tail.
    def enterTail(self, ctx:CNTRParser.TailContext):
        pass

    # Exit a parse tree produced by CNTRParser#tail.
    def exitTail(self, ctx:CNTRParser.TailContext):
        pass


    # Enter a parse tree produced by CNTRParser#string.
    def enterString(self, ctx:CNTRParser.StringContext):
        pass

    # Exit a parse tree produced by CNTRParser#string.
    def exitString(self, ctx:CNTRParser.StringContext):
        pass


    # Enter a parse tree produced by CNTRParser#block.
    def enterBlock(self, ctx:CNTRParser.BlockContext):
        pass

    # Exit a parse tree produced by CNTRParser#block.
    def exitBlock(self, ctx:CNTRParser.BlockContext):
        pass


    # Enter a parse tree produced by CNTRParser#blocks.
    def enterBlocks(self, ctx:CNTRParser.BlocksContext):
        pass

    # Exit a parse tree produced by CNTRParser#blocks.
    def exitBlocks(self, ctx:CNTRParser.BlocksContext):
        pass


    # Enter a parse tree produced by CNTRParser#verse.
    def enterVerse(self, ctx:CNTRParser.VerseContext):
        pass

    # Exit a parse tree produced by CNTRParser#verse.
    def exitVerse(self, ctx:CNTRParser.VerseContext):
        pass


    # Enter a parse tree produced by CNTRParser#lineBreak.
    def enterLineBreak(self, ctx:CNTRParser.LineBreakContext):
        pass

    # Exit a parse tree produced by CNTRParser#lineBreak.
    def exitLineBreak(self, ctx:CNTRParser.LineBreakContext):
        pass


    # Enter a parse tree produced by CNTRParser#alternateVersification.
    def enterAlternateVersification(self, ctx:CNTRParser.AlternateVersificationContext):
        pass

    # Exit a parse tree produced by CNTRParser#alternateVersification.
    def exitAlternateVersification(self, ctx:CNTRParser.AlternateVersificationContext):
        pass


    # Enter a parse tree produced by CNTRParser#characterMissing.
    def enterCharacterMissing(self, ctx:CNTRParser.CharacterMissingContext):
        pass

    # Exit a parse tree produced by CNTRParser#characterMissing.
    def exitCharacterMissing(self, ctx:CNTRParser.CharacterMissingContext):
        pass


    # Enter a parse tree produced by CNTRParser#numericAbbreviation.
    def enterNumericAbbreviation(self, ctx:CNTRParser.NumericAbbreviationContext):
        pass

    # Exit a parse tree produced by CNTRParser#numericAbbreviation.
    def exitNumericAbbreviation(self, ctx:CNTRParser.NumericAbbreviationContext):
        pass


    # Enter a parse tree produced by CNTRParser#pageBreak.
    def enterPageBreak(self, ctx:CNTRParser.PageBreakContext):
        pass

    # Exit a parse tree produced by CNTRParser#pageBreak.
    def exitPageBreak(self, ctx:CNTRParser.PageBreakContext):
        pass


    # Enter a parse tree produced by CNTRParser#characterDamaged.
    def enterCharacterDamaged(self, ctx:CNTRParser.CharacterDamagedContext):
        pass

    # Exit a parse tree produced by CNTRParser#characterDamaged.
    def exitCharacterDamaged(self, ctx:CNTRParser.CharacterDamagedContext):
        pass


    # Enter a parse tree produced by CNTRParser#columnBreak.
    def enterColumnBreak(self, ctx:CNTRParser.ColumnBreakContext):
        pass

    # Exit a parse tree produced by CNTRParser#columnBreak.
    def exitColumnBreak(self, ctx:CNTRParser.ColumnBreakContext):
        pass


    # Enter a parse tree produced by CNTRParser#wordSuppliedByVid.
    def enterWordSuppliedByVid(self, ctx:CNTRParser.WordSuppliedByVidContext):
        pass

    # Exit a parse tree produced by CNTRParser#wordSuppliedByVid.
    def exitWordSuppliedByVid(self, ctx:CNTRParser.WordSuppliedByVidContext):
        pass


    # Enter a parse tree produced by CNTRParser#lineRemnant.
    def enterLineRemnant(self, ctx:CNTRParser.LineRemnantContext):
        pass

    # Exit a parse tree produced by CNTRParser#lineRemnant.
    def exitLineRemnant(self, ctx:CNTRParser.LineRemnantContext):
        pass


    # Enter a parse tree produced by CNTRParser#verseRemnant.
    def enterVerseRemnant(self, ctx:CNTRParser.VerseRemnantContext):
        pass

    # Exit a parse tree produced by CNTRParser#verseRemnant.
    def exitVerseRemnant(self, ctx:CNTRParser.VerseRemnantContext):
        pass


    # Enter a parse tree produced by CNTRParser#wordSupplied.
    def enterWordSupplied(self, ctx:CNTRParser.WordSuppliedContext):
        pass

    # Exit a parse tree produced by CNTRParser#wordSupplied.
    def exitWordSupplied(self, ctx:CNTRParser.WordSuppliedContext):
        pass


    # Enter a parse tree produced by CNTRParser#nominaSacra.
    def enterNominaSacra(self, ctx:CNTRParser.NominaSacraContext):
        pass

    # Exit a parse tree produced by CNTRParser#nominaSacra.
    def exitNominaSacra(self, ctx:CNTRParser.NominaSacraContext):
        pass


    # Enter a parse tree produced by CNTRParser#count.
    def enterCount(self, ctx:CNTRParser.CountContext):
        pass

    # Exit a parse tree produced by CNTRParser#count.
    def exitCount(self, ctx:CNTRParser.CountContext):
        pass


    # Enter a parse tree produced by CNTRParser#empty.
    def enterEmpty(self, ctx:CNTRParser.EmptyContext):
        pass

    # Exit a parse tree produced by CNTRParser#empty.
    def exitEmpty(self, ctx:CNTRParser.EmptyContext):
        pass


    # Enter a parse tree produced by CNTRParser#editedTextBody.
    def enterEditedTextBody(self, ctx:CNTRParser.EditedTextBodyContext):
        pass

    # Exit a parse tree produced by CNTRParser#editedTextBody.
    def exitEditedTextBody(self, ctx:CNTRParser.EditedTextBodyContext):
        pass


    # Enter a parse tree produced by CNTRParser#editedText.
    def enterEditedText(self, ctx:CNTRParser.EditedTextContext):
        pass

    # Exit a parse tree produced by CNTRParser#editedText.
    def exitEditedText(self, ctx:CNTRParser.EditedTextContext):
        pass


    # Enter a parse tree produced by CNTRParser#editedTextContent.
    def enterEditedTextContent(self, ctx:CNTRParser.EditedTextContentContext):
        pass

    # Exit a parse tree produced by CNTRParser#editedTextContent.
    def exitEditedTextContent(self, ctx:CNTRParser.EditedTextContentContext):
        pass


    # Enter a parse tree produced by CNTRParser#first.
    def enterFirst(self, ctx:CNTRParser.FirstContext):
        pass

    # Exit a parse tree produced by CNTRParser#first.
    def exitFirst(self, ctx:CNTRParser.FirstContext):
        pass


    # Enter a parse tree produced by CNTRParser#uncorrected.
    def enterUncorrected(self, ctx:CNTRParser.UncorrectedContext):
        pass

    # Exit a parse tree produced by CNTRParser#uncorrected.
    def exitUncorrected(self, ctx:CNTRParser.UncorrectedContext):
        pass


    # Enter a parse tree produced by CNTRParser#corrected.
    def enterCorrected(self, ctx:CNTRParser.CorrectedContext):
        pass

    # Exit a parse tree produced by CNTRParser#corrected.
    def exitCorrected(self, ctx:CNTRParser.CorrectedContext):
        pass


    # Enter a parse tree produced by CNTRParser#second.
    def enterSecond(self, ctx:CNTRParser.SecondContext):
        pass

    # Exit a parse tree produced by CNTRParser#second.
    def exitSecond(self, ctx:CNTRParser.SecondContext):
        pass


    # Enter a parse tree produced by CNTRParser#third.
    def enterThird(self, ctx:CNTRParser.ThirdContext):
        pass

    # Exit a parse tree produced by CNTRParser#third.
    def exitThird(self, ctx:CNTRParser.ThirdContext):
        pass


    # Enter a parse tree produced by CNTRParser#reference.
    def enterReference(self, ctx:CNTRParser.ReferenceContext):
        pass

    # Exit a parse tree produced by CNTRParser#reference.
    def exitReference(self, ctx:CNTRParser.ReferenceContext):
        pass


    # Enter a parse tree produced by CNTRParser#chapterNumber.
    def enterChapterNumber(self, ctx:CNTRParser.ChapterNumberContext):
        pass

    # Exit a parse tree produced by CNTRParser#chapterNumber.
    def exitChapterNumber(self, ctx:CNTRParser.ChapterNumberContext):
        pass


    # Enter a parse tree produced by CNTRParser#verseNumber.
    def enterVerseNumber(self, ctx:CNTRParser.VerseNumberContext):
        pass

    # Exit a parse tree produced by CNTRParser#verseNumber.
    def exitVerseNumber(self, ctx:CNTRParser.VerseNumberContext):
        pass


    # Enter a parse tree produced by CNTRParser#bookNumber.
    def enterBookNumber(self, ctx:CNTRParser.BookNumberContext):
        pass

    # Exit a parse tree produced by CNTRParser#bookNumber.
    def exitBookNumber(self, ctx:CNTRParser.BookNumberContext):
        pass



del CNTRParser